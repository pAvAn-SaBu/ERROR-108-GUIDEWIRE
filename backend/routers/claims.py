"""
routers/claims.py
-----------------
POST /claims/process — Full parametric claim pipeline:
  1. Check active triggers (Isolation Forest)
  2. Compute risk score (GB+RF)
  3. Evaluate fraud (OC-SVM ensemble)
  4. Decide payout amount based on plan
  5. Update trust score
"""

from fastapi import APIRouter, HTTPException
from schemas.models import ClaimProcessRequest, ClaimProcessResponse, FraudTier
from models.anomaly_detector import check_triggers
from models.risk_engine import compute_risk
from models.fraud_detector import evaluate_fraud
from models.trust_engine import update_trust

router = APIRouter(prefix="/claims", tags=["Claims"])

PLAN_COVERAGE = {
    "basic":    1000,
    "standard": 2000,
    "premium":  3000,
}

# Payout as % of coverage based on disruption severity
PAYOUT_RATES = {
    "alert":   0.70,   # 70% of weekly coverage
    "warning": 0.40,
    "normal":  0.00,
}


@router.post("/process", response_model=ClaimProcessResponse, summary="Process a parametric claim end-to-end")
def process_claim(req: ClaimProcessRequest):
    """
    Full automated claim pipeline:

    1. **Trigger Check** – Isolation Forest anomaly detection
    2. **Risk Score**   – GB+RF ensemble for the worker's city
    3. **Fraud Check**  – 6-signal OC-SVM evaluation
    4. **Payout Calc**  – parametric amount from trigger severity × plan coverage
    5. **Trust Update** – Bayesian trust score updated post-claim
    """

    # ── Step 1: Trigger detection ──────────────────────────────────────────
    trigger_result = check_triggers(req.city.value)
    active_trigger = next(
        (t for t in trigger_result["triggers"] if t["status"] in ("alert", "warning")),
        None
    )

    if active_trigger is None:
        raise HTTPException(
            status_code=422,
            detail="No active environmental trigger detected for this city. Claim cannot be processed."
        )

    # ── Step 2: Risk score ────────────────────────────────────────────────
    risk = compute_risk(
        city=req.city.value,
        platform=req.platform.value,
        weekly_income=req.weekly_income,
        month=req.month,
    )

    # ── Step 3: Fraud evaluation ──────────────────────────────────────────
    signals_dict = {
        "gps":     req.signals.gps_consistency,
        "motion":  req.signals.motion_pattern,
        "network": req.signals.network_degradation,
        "platform":req.signals.platform_activity,
        "device":  req.signals.device_fingerprint,
        "cluster": req.signals.cluster_risk,
    }

    coverage     = PLAN_COVERAGE.get(req.plan.value, 2000)
    claim_amount = int(coverage * PAYOUT_RATES.get(active_trigger["status"], 0))

    fraud = evaluate_fraud(
        worker_id=req.worker_id,
        city=req.city.value,
        trust_score=req.trust_score,
        signals_in=signals_dict,
        claim_amount=claim_amount,
    )

    fraud_tier = fraud["tier"]

    # ── Step 4: Payout decision ───────────────────────────────────────────
    if fraud_tier == "green":
        claim_approved = True
        payout_amount  = claim_amount
        explanation    = (
            f"Trigger '{active_trigger['name']}' confirmed anomalous "
            f"(score={active_trigger['anomaly_score']:.2f}). All 6 fraud signals cleared. "
            f"₹{payout_amount} auto-approved."
        )
        next_action = "Payout sent via UPI instantly."
    elif fraud_tier == "yellow":
        claim_approved = False
        payout_amount  = 0
        explanation    = (
            f"Trigger confirmed but fraud signals ambiguous. "
            f"Soft hold — secondary verification needed."
        )
        next_action = "Worker must confirm via photo or wait for GPS re-check (10–15 min)."
    else:  # red
        claim_approved = False
        payout_amount  = 0
        explanation    = (
            f"Multiple fraud signals inconsistent. Claim flagged for manual review."
        )
        next_action = "Human reviewer will verify within 2 hours. Appeal available."

    # ── Step 5: Trust update ──────────────────────────────────────────────
    update_trust(
        worker_id=req.worker_id,
        claim_verified=claim_approved,
        was_flagged=(fraud_tier == "red"),
        payout_amount=payout_amount,
    )

    return ClaimProcessResponse(
        worker_id=req.worker_id,
        claim_approved=claim_approved,
        payout_amount=payout_amount,
        fraud_tier=FraudTier(fraud_tier),
        risk_score=risk["risk_score"],
        trigger_event=f"{active_trigger['name']} — {active_trigger['label']} "
                      f"({active_trigger['current_value']} {active_trigger['unit']})",
        fraud_score=fraud["fraud_score"],
        explanation=explanation,
        next_action=next_action,
    )
