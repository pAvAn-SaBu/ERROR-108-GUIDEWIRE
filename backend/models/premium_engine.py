"""
models/premium_engine.py
------------------------
Dynamic premium calculator. Takes the ML risk score and computes
risk-adjusted weekly premiums for each plan tier.
Base premiums: Basic ₹30, Standard ₹50, Premium ₹70
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

BASE_PLANS = [
    {"plan": "basic",    "base_premium": 30,  "coverage": 1000},
    {"plan": "standard", "base_premium": 50,  "coverage": 2000},
    {"plan": "premium",  "base_premium": 70,  "coverage": 3000},
]

# Income-exposure multiplier: higher earners need proportionally more coverage
INCOME_BRACKETS = [
    (3000,  0.90),
    (5000,  0.95),
    (7000,  1.00),
    (10000, 1.08),
    (15000, 1.15),
]


def _income_multiplier(weekly_income: int) -> float:
    for threshold, mult in INCOME_BRACKETS:
        if weekly_income <= threshold:
            return mult
    return 1.20


def calculate_premiums(city: str, risk_score: float, weekly_income: int) -> dict:
    """
    Returns adjusted premiums for all three plan tiers.

    Adjustment formula:
      if risk_score > 0.50:  adjustment = +0.45 * (risk_score - 0.50)   [surcharge]
      if risk_score < 0.45:  adjustment = -0.35 * (0.45 - risk_score)   [discount]
      else:                   adjustment = 0                              [base rate]

    Income multiplier applied on top.
    """
    # Risk adjustment factor
    if risk_score > 0.50:
        risk_adj = 0.45 * (risk_score - 0.50)      # up to +~22.5% surcharge
    elif risk_score < 0.45:
        risk_adj = -0.35 * (0.45 - risk_score)     # up to ~-16% discount
    else:
        risk_adj = 0.0

    income_mult = _income_multiplier(weekly_income)

    plans = []
    for p in BASE_PLANS:
        raw       = p["base_premium"] * (1 + risk_adj) * income_mult
        adjusted  = int(round(raw / 5) * 5)    # round to nearest ₹5
        discount  = round((adjusted - p["base_premium"]) / p["base_premium"] * 100, 1)

        plans.append({
            "plan":             p["plan"],
            "base_premium":     p["base_premium"],
            "adjusted_premium": adjusted,
            "coverage":         p["coverage"],
            "discount_pct":     discount,
        })

    return {
        "city":                   city,
        "risk_score":             round(risk_score, 4),
        "plans":                  plans,
        "risk_adjustment_factor": round(risk_adj, 4),
    }
