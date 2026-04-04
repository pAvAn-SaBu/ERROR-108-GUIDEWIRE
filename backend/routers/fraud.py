"""
routers/fraud.py
----------------
POST /fraud/evaluate  — Multi-signal fraud evaluation
GET  /trust/{worker_id} — Trust score lookup
POST /trust/update    — Update trust after claim outcome
"""

from fastapi import APIRouter
from schemas.models import (
    FraudEvaluateRequest, FraudEvaluateResponse,
    SignalResult, FraudTier,
    TrustUpdateRequest, TrustScoreResponse,
)
from models.fraud_detector import evaluate_fraud
from models.trust_engine import compute_trust, update_trust

router = APIRouter(tags=["Fraud & Trust"])


@router.post("/fraud/evaluate", response_model=FraudEvaluateResponse, summary="Multi-signal fraud evaluation")
def fraud_evaluate(req: FraudEvaluateRequest):
    """
    Evaluates a claim using 6 behavioral signals via a One-Class SVM
    trained on legitimate claim fingerprints, combined with a weighted
    ensemble scorer.

    Returns fraud_score (0=legit → 1=fraud), tier (green/yellow/red),
    per-signal confidence scores, and recommended action.
    """
    signals_dict = {
        "gps":     req.signals.gps_consistency,
        "motion":  req.signals.motion_pattern,
        "network": req.signals.network_degradation,
        "platform":req.signals.platform_activity,
        "device":  req.signals.device_fingerprint,
        "cluster": req.signals.cluster_risk,
    }

    result = evaluate_fraud(
        worker_id=req.worker_id,
        city=req.city.value,
        trust_score=req.trust_score,
        signals_in=signals_dict,
        claim_amount=req.claim_amount,
    )

    return FraudEvaluateResponse(
        worker_id=result["worker_id"],
        fraud_score=result["fraud_score"],
        tier=FraudTier(result["tier"]),
        signals=[SignalResult(**s) for s in result["signals"]],
        confidence=result["confidence"],
        explanation=result["explanation"],
        recommended_action=result["recommended_action"],
    )


@router.get("/trust/{worker_id}", response_model=TrustScoreResponse, summary="Get worker trust score")
def get_trust(worker_id: str):
    """
    Returns the Bayesian trust score (0–100) for a worker based on
    their claim history, account age, and false-flag record.
    """
    result = compute_trust(worker_id)
    return TrustScoreResponse(**result)


@router.post("/trust/update", response_model=TrustScoreResponse, summary="Update trust after claim outcome")
def update_trust_endpoint(req: TrustUpdateRequest):
    """
    Updates the worker's trust record after a claim is resolved and
    returns the recalculated trust score.
    """
    result = update_trust(
        worker_id=req.worker_id,
        claim_verified=req.claim_verified,
        was_flagged=req.was_flagged,
        payout_amount=req.payout_amount,
    )
    return TrustScoreResponse(**result)
