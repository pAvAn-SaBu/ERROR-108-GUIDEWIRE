"""
routers/risk.py
---------------
/risk/score   — ML risk score for a worker
/premium/calculate — dynamic adjusted premiums
"""

from fastapi import APIRouter
from schemas.models import (
    RiskScoreRequest, RiskScoreResponse,
    PremiumCalculateRequest, PremiumCalculateResponse,
    FeatureImportance, PlanPremium,
    RiskLabel,
)
from models.risk_engine import compute_risk
from models.premium_engine import calculate_premiums

router = APIRouter(prefix="/risk", tags=["Risk & Premium"])


@router.post("/score", response_model=RiskScoreResponse, summary="Compute ML risk score")
def risk_score(req: RiskScoreRequest):
    """
    Uses a Gradient Boosting + Random Forest ensemble trained on
    synthetic Indian city weather and AQI data to predict a
    location-based disruption risk score (0–1) for the worker.
    """
    result = compute_risk(
        city=req.city.value,
        platform=req.platform.value,
        weekly_income=req.weekly_income,
        month=req.month,
    )
    return RiskScoreResponse(
        city=result["city"],
        risk_score=result["risk_score"],
        risk_label=RiskLabel(result["risk_label"]),
        confidence_interval=result["confidence_interval"],
        feature_importances=[FeatureImportance(**f) for f in result["feature_importances"]],
        disruption_prob=result["disruption_prob"],
        model_used=result["model_used"],
    )


premium_router = APIRouter(prefix="/premium", tags=["Risk & Premium"])


@premium_router.post("/calculate", response_model=PremiumCalculateResponse, summary="Get risk-adjusted premiums")
def premium_calculate(req: PremiumCalculateRequest):
    """
    Returns weekly premiums for Basic / Standard / Premium plans
    adjusted for the worker's city risk score and income level.
    Low-risk cities get discounts; high-risk gets a surcharge.
    """
    result = calculate_premiums(
        city=req.city.value,
        risk_score=req.risk_score,
        weekly_income=req.weekly_income,
    )
    return PremiumCalculateResponse(
        city=result["city"],
        risk_score=result["risk_score"],
        plans=[PlanPremium(**p) for p in result["plans"]],
        risk_adjustment_factor=result["risk_adjustment_factor"],
    )
