"""
routers/triggers.py
-------------------
GET /triggers/{city}  — Isolation Forest anomaly detection on live weather sim
"""

from fastapi import APIRouter, Path
from schemas.models import TriggersResponse, TriggerDetail, TriggerStatus
from models.anomaly_detector import check_triggers

router = APIRouter(prefix="/triggers", tags=["Trigger Detection"])

VALID_CITIES = ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad"]


@router.get("/{city}", response_model=TriggersResponse, summary="Get live trigger anomaly status")
def get_triggers(
    city: str = Path(..., description="City name", example="Bangalore")
):
    """
    Runs the Isolation Forest model trained on historical 'normal' weather
    for the given city and scores current simulated conditions.

    Returns trigger statuses (normal / warning / alert) for:
    - Rainfall
    - AQI (Air Quality Index)
    - Temperature / Heat
    - Wind Speed
    """
    if city not in VALID_CITIES:
        city = "Bangalore"

    result = check_triggers(city)

    triggers = [
        TriggerDetail(
            name=t["name"],
            status=TriggerStatus(t["status"]),
            label=t["label"],
            anomaly_score=t["anomaly_score"],
            current_value=t["current_value"],
            unit=t["unit"],
            threshold=t["threshold"],
            description=t["description"],
        )
        for t in result["triggers"]
    ]

    return TriggersResponse(
        city=result["city"],
        triggers=triggers,
        any_alert=result["any_alert"],
        model_used=result["model_used"],
    )
