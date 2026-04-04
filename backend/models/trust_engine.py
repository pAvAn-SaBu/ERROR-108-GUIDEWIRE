"""
models/trust_engine.py
----------------------
Bayesian trust score engine. Scores workers 0–100 based on their
claim history. Higher trust reduces fraud scrutiny thresholds and
can unlock premium discounts.
"""

import math
from typing import Literal

# ── In-memory worker store (replace with DB in production) ───────────────────
_worker_store: dict[str, dict] = {}

TIER_THRESHOLDS = [
    (85, "platinum"),
    (65, "gold"),
    (40, "silver"),
    (0,  "bronze"),
]

def _get_tier(score: float) -> str:
    for threshold, tier in TIER_THRESHOLDS:
        if score >= threshold:
            return tier
    return "bronze"

def _get_or_create(worker_id: str) -> dict:
    if worker_id not in _worker_store:
        _worker_store[worker_id] = {
            "total_claims":    0,
            "verified_claims": 0,
            "false_flags":     0,
            "total_payout":    0,
            "account_days":    90,   # default onboarding age
        }
    return _worker_store[worker_id]


def compute_trust(worker_id: str) -> dict:
    """
    Compute trust score using a Bayesian Beta-distribution estimator.

    Base formula:
      alpha = verified_claims + 1       (successes + prior)
      beta  = (total - verified) + 1    (failures + prior)
      mean  = alpha / (alpha + beta)    → maps to 0–1

    Penalties: false flags reduce score.
    Bonuses: account age, high payout history.
    """
    w = _get_or_create(worker_id)

    alpha = w["verified_claims"] + 1.0
    beta  = max((w["total_claims"] - w["verified_claims"]) + 1.0, 1.0)
    base  = alpha / (alpha + beta)

    # Age bonus: up to +5 points for accounts > 6 months
    age_bonus = min(w["account_days"] / 365.0 * 5.0, 5.0)

    # False flag penalty: each flag costs 8 points
    flag_penalty = w["false_flags"] * 8.0

    # Payout history signal: loyal customers with repeated claims
    payout_bonus = min(math.log1p(w["total_payout"] / 1000.0) * 2.0, 8.0)

    raw_score = base * 100.0 + age_bonus + payout_bonus - flag_penalty
    score     = round(max(0.0, min(100.0, raw_score)), 2)

    # Trend: compare to last snapshot (simplified)
    prev_score = w.get("last_score", score)
    if score > prev_score + 1:
        trend = "improving"
    elif score < prev_score - 1:
        trend = "declining"
    else:
        trend = "stable"

    w["last_score"] = score
    tier = _get_tier(score)

    # Percentile: sigmoid approximation
    percentile = round(100 / (1 + math.exp(-0.08 * (score - 50))), 1)

    bonuses = []
    if w["verified_claims"] >= 5:
        bonuses.append("Veteran Claimer — 5+ verified claims")
    if w["false_flags"] == 0:
        bonuses.append("Clean Record — zero false flags")
    if w["account_days"] > 180:
        bonuses.append("Loyal Member — 6+ months active")
    if score >= 80:
        bonuses.append("Premium Eligibility — reduced fraud scrutiny")

    tier_descs = {
        "platinum": "Platinum tier: maximum trust, instant payouts, lowest premiums.",
        "gold":     "Gold tier: high trust, expedited claims, minor premium discount.",
        "silver":   "Silver tier: standard trust level, normal claims process.",
        "bronze":   "Bronze tier: new or limited history, standard scrutiny applied.",
    }

    return {
        "worker_id":   worker_id,
        "score":       score,
        "tier":        tier,
        "percentile":  percentile,
        "trend":       trend,
        "bonuses":     bonuses,
        "description": tier_descs[tier],
    }


def update_trust(worker_id: str, claim_verified: bool, was_flagged: bool, payout_amount: int) -> dict:
    """
    Update trust record after a claim outcome and return the new score.
    """
    w = _get_or_create(worker_id)
    w["total_claims"]    += 1
    w["total_payout"]    += payout_amount if claim_verified else 0
    w["account_days"]    += 7   # one week elapsed

    if claim_verified:
        w["verified_claims"] += 1
    if was_flagged and not claim_verified:
        w["false_flags"] += 1

    return compute_trust(worker_id)
