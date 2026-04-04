"""
schemas/models.py
-----------------
Pydantic v2 request and response schemas for all Revo API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional
from enum import Enum


# ── Shared enums ───────────────────────────────────────────────────────────────

class City(str, Enum):
    bangalore = "Bangalore"
    mumbai    = "Mumbai"
    delhi     = "Delhi"
    chennai   = "Chennai"
    hyderabad = "Hyderabad"

class Platform(str, Enum):
    swiggy  = "Swiggy"
    zomato  = "Zomato"
    blinkit = "Blinkit"
    zepto   = "Zepto"
    dunzo   = "Dunzo"

class RiskLabel(str, Enum):
    low    = "Low"
    medium = "Medium"
    high   = "High"

class TriggerStatus(str, Enum):
    normal  = "normal"
    warning = "warning"
    alert   = "alert"

class FraudTier(str, Enum):
    green  = "green"
    yellow = "yellow"
    red    = "red"

class PlanTier(str, Enum):
    basic    = "basic"
    standard = "standard"
    premium  = "premium"


# ── /risk/score ────────────────────────────────────────────────────────────────

class RiskScoreRequest(BaseModel):
    city:          City     = Field(..., example="Bangalore")
    platform:      Platform = Field(..., example="Swiggy")
    weekly_income: int      = Field(..., ge=1000, le=50000, example=6000)
    month:         int      = Field(..., ge=1, le=12, example=7)

class FeatureImportance(BaseModel):
    feature: str
    importance: float
    contribution: float

class RiskScoreResponse(BaseModel):
    city:                 str
    risk_score:           float = Field(..., ge=0, le=1)
    risk_label:           RiskLabel
    confidence_interval:  tuple[float, float]
    feature_importances:  list[FeatureImportance]
    disruption_prob:      float   # P(disruption event in next 7 days)
    model_used:           str


# ── /premium/calculate ─────────────────────────────────────────────────────────

class PremiumCalculateRequest(BaseModel):
    city:          City
    risk_score:    float = Field(..., ge=0, le=1)
    weekly_income: int   = Field(..., ge=1000, le=50000)

class PlanPremium(BaseModel):
    plan:          PlanTier
    base_premium:  int
    adjusted_premium: int
    coverage:      int
    discount_pct:  float   # negative = surcharge

class PremiumCalculateResponse(BaseModel):
    city:          str
    risk_score:    float
    plans:         list[PlanPremium]
    risk_adjustment_factor: float


# ── /triggers/{city} ──────────────────────────────────────────────────────────

class TriggerDetail(BaseModel):
    name:          str
    status:        TriggerStatus
    label:         str
    anomaly_score: float          # 0 = normal, 1 = extreme anomaly
    current_value: float
    unit:          str
    threshold:     float
    description:   str

class TriggersResponse(BaseModel):
    city:        str
    triggers:    list[TriggerDetail]
    any_alert:   bool
    model_used:  str


# ── /fraud/evaluate ───────────────────────────────────────────────────────────

class SignalInput(BaseModel):
    gps_consistency:      float = Field(..., ge=0, le=1, description="0=spoofed, 1=genuine trajectory")
    motion_pattern:       float = Field(..., ge=0, le=1, description="Device accelerometer activity score")
    network_degradation:  float = Field(..., ge=0, le=1, description="1=signal strongly degraded, 0=normal")
    platform_activity:    float = Field(..., ge=0, le=1, description="Matched delivery activity during event")
    device_fingerprint:   float = Field(..., ge=0, le=1, description="Hardware consistency score")
    cluster_risk:         float = Field(..., ge=0, le=1, description="0=isolated claim, 1=cluster ring")

class FraudEvaluateRequest(BaseModel):
    worker_id:     str
    city:          City
    trust_score:   float = Field(default=50.0, ge=0, le=100)
    signals:       SignalInput
    claim_amount:  int = Field(..., ge=100, le=5000)

class SignalResult(BaseModel):
    key:           str
    label:         str
    confidence:    float          # 0–1
    passed:        bool
    weight:        float
    explanation:   str

class FraudEvaluateResponse(BaseModel):
    worker_id:   str
    fraud_score: float            # 0=legitimate, 1=fraudulent
    tier:        FraudTier
    signals:     list[SignalResult]
    confidence:  float
    explanation: str
    recommended_action: str


# ── /claims/process ───────────────────────────────────────────────────────────

class ClaimProcessRequest(BaseModel):
    worker_id:     str
    city:          City
    platform:      Platform
    weekly_income: int
    plan:          PlanTier
    trust_score:   float = Field(default=50.0, ge=0, le=100)
    signals:       SignalInput
    month:         int = Field(..., ge=1, le=12)

class ClaimProcessResponse(BaseModel):
    worker_id:      str
    claim_approved: bool
    payout_amount:  int
    fraud_tier:     FraudTier
    risk_score:     float
    trigger_event:  Optional[str]
    fraud_score:    float
    explanation:    str
    next_action:    str


# ── /trust/{worker_id} ────────────────────────────────────────────────────────

class TrustUpdateRequest(BaseModel):
    worker_id:      str
    claim_verified: bool
    was_flagged:    bool
    payout_amount:  int

class TrustScoreResponse(BaseModel):
    worker_id:   str
    score:       float   # 0–100
    tier:        Literal["bronze", "silver", "gold", "platinum"]
    percentile:  float
    trend:       Literal["improving", "stable", "declining"]
    bonuses:     list[str]
    description: str
