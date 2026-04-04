"""
models/fraud_detector.py
------------------------
Multi-signal fraud detection engine using a One-Class SVM trained on
legitimate claim patterns, combined with a weighted rule-based ensemble
for each of the 6 behavioral signals.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler

# ── Signal definitions ────────────────────────────────────────────────────────

SIGNALS = [
    {
        "key":    "gps",
        "label":  "GPS Consistency",
        "weight": 0.25,
        "desc_pass": "GPS trajectory matches expected delivery pattern",
        "desc_fail": "GPS path inconsistent — possible location spoofing",
    },
    {
        "key":    "motion",
        "label":  "Device Motion Pattern",
        "weight": 0.15,
        "desc_pass": "Accelerometer shows active movement consistent with delivery",
        "desc_fail": "Device appears stationary despite claimed delivery activity",
    },
    {
        "key":    "network",
        "label":  "Network Signal Degraded",
        "weight": 0.15,
        "desc_pass": "Network degradation correlates with weather disruption event",
        "desc_fail": "Network signal normal — does not align with claimed disruption",
    },
    {
        "key":    "platform",
        "label":  "Platform Activity Match",
        "weight": 0.25,
        "desc_pass": "Delivery app shows reduced orders matching disruption window",
        "desc_fail": "Platform logs show normal order volume — disruption unconfirmed",
    },
    {
        "key":    "device",
        "label":  "Device Fingerprint",
        "weight": 0.10,
        "desc_pass": "Device hardware profile consistent with registered account",
        "desc_fail": "Device fingerprint mismatch — possible shared-device fraud",
    },
    {
        "key":    "cluster",
        "label":  "No Cluster Ring Detected",
        "weight": 0.10,
        "desc_pass": "No coordinated claim ring detected in vicinity",
        "desc_fail": "Multiple simultaneous claims from same zone — cluster risk elevated",
    },
]

SIGNAL_KEYS  = [s["key"] for s in SIGNALS]
SIGNAL_MAP   = {s["key"]: s for s in SIGNALS}

# ── One-Class SVM trained on legitimate signal patterns ───────────────────────

_ocsvm: OneClassSVM | None = None
_scaler: StandardScaler | None = None


def _train_ocsvm():
    """
    Generate synthetic 'normal' (legitimate) signal fingerprints and train
    a One-Class SVM to identify the boundary of legitimate behaviour.
    """
    global _ocsvm, _scaler
    rng = np.random.default_rng(42)
    n = 1000

    # Legitimate claim profile:
    #   gps: high (0.75–1.0), motion: moderate-high (0.6–1.0),
    #   network: moderate-high (0.5–1.0), platform: high (0.7–1.0),
    #   device: high (0.85–1.0), cluster: low (0–0.15)
    legit = np.column_stack([
        rng.uniform(0.72, 1.0,  n),   # gps
        rng.uniform(0.55, 1.0,  n),   # motion
        rng.uniform(0.45, 1.0,  n),   # network (higher = more degraded = consistent)
        rng.uniform(0.68, 1.0,  n),   # platform
        rng.uniform(0.82, 1.0,  n),   # device
        rng.uniform(0.0,  0.18, n),   # cluster (low = no ring)
    ])

    _scaler = StandardScaler()
    X_scaled = _scaler.fit_transform(legit)

    _ocsvm = OneClassSVM(kernel="rbf", gamma="scale", nu=0.08)
    _ocsvm.fit(X_scaled)


def _get_ocsvm():
    global _ocsvm, _scaler
    if _ocsvm is None:
        _train_ocsvm()
    return _ocsvm, _scaler


def _score_signal(key: str, raw_value: float) -> tuple[float, bool]:
    """
    Converts a raw signal value to a confidence score and pass/fail.
    For 'cluster': inverted (low input = high confidence = pass).
    """
    if key == "cluster":
        confidence = 1.0 - raw_value        # low cluster risk → high confidence
        passed     = raw_value < 0.25
    elif key == "network":
        confidence = raw_value              # high degradation → consistent with event
        passed     = raw_value > 0.40
    else:
        confidence = raw_value
        passed     = raw_value > 0.60

    return round(float(confidence), 4), bool(passed)


def evaluate_fraud(
    worker_id:    str,
    city:         str,
    trust_score:  float,
    signals_in:   dict,       # keys: gps, motion, network, platform, device, cluster
    claim_amount: int,
) -> dict:
    """
    Main entry point. Returns full fraud evaluation result.
    """
    ocsvm, scaler = _get_ocsvm()

    # Build signal results
    signal_results = []
    weighted_conf  = 0.0
    total_weight   = 0.0

    for sig in SIGNALS:
        key     = sig["key"]
        raw_val = float(signals_in.get(key, 0.5))
        conf, passed = _score_signal(key, raw_val)

        signal_results.append({
            "key":         key,
            "label":       sig["label"],
            "confidence":  conf,
            "passed":      passed,
            "weight":      sig["weight"],
            "explanation": sig["desc_pass"] if passed else sig["desc_fail"],
        })
        weighted_conf += conf * sig["weight"]
        total_weight  += sig["weight"]

    ensemble_score = weighted_conf / total_weight  # legitimacy score (higher = more legit)

    # One-Class SVM refinement
    feature_vec = np.array([[signals_in.get(k, 0.5) for k in SIGNAL_KEYS]])
    X_scaled    = scaler.transform(feature_vec)
    ocsvm_pred  = ocsvm.predict(X_scaled)[0]   # 1 = inlier (legit), -1 = outlier (fraud)
    ocsvm_score = float(ocsvm.score_samples(X_scaled)[0])

    # Normalize OCSVM score contribution
    ocsvm_legit = float(np.clip((ocsvm_score + 0.5) / 1.0, 0, 1))

    # Final fraud score (0=legit → 1=fraud) — inverted from legitimacy
    legitimacy = 0.65 * ensemble_score + 0.35 * ocsvm_legit
    # Trust score bonus: high trust workers get slight benefit of doubt
    trust_bonus = (trust_score - 50) / 500.0    # ±0.1 adjustment
    legitimacy  = float(np.clip(legitimacy + trust_bonus, 0, 1))
    fraud_score = round(1.0 - legitimacy, 4)

    # Claim-size surcharge: large claims raise scrutiny slightly
    if claim_amount > 1500:
        fraud_score = min(fraud_score + 0.04, 1.0)

    # Tier assignment
    if fraud_score < 0.28:
        tier               = "green"
        recommended_action = "Auto-approve payout via UPI"
        top_explanation    = "All signals consistent with genuine disruption. Payout approved."
    elif fraud_score < 0.55:
        tier               = "yellow"
        recommended_action = "Request photo confirmation or wait 15 min for GPS re-check"
        top_explanation    = "One or more signals ambiguous. Soft hold pending secondary verification."
    else:
        tier               = "red"
        recommended_action = "Escalate to human reviewer within 2 hours"
        top_explanation    = "Multiple signals inconsistent. Claim flagged for manual review."

    return {
        "worker_id":          worker_id,
        "fraud_score":        round(fraud_score, 4),
        "tier":               tier,
        "signals":            signal_results,
        "confidence":         round(1.0 - abs(fraud_score - 0.5) * 2, 4),
        "explanation":        top_explanation,
        "recommended_action": recommended_action,
    }
