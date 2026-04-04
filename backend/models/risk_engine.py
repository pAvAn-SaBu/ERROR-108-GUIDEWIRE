"""
models/risk_engine.py
---------------------
Risk Prediction Engine using a Gradient Boosting + Random Forest ensemble.
Trained on synthetic Indian city weather data. Returns risk score (0–1),
label, feature importances, and disruption probability.
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from data.synthetic_data import (
    generate_training_data,
    get_feature_columns,
    get_city_profile,
    CITY_PROFILES,
    PLATFORM_ENCODE,
    SEASON_ENCODE,
)

# ── Singleton: train once on module load ──────────────────────────────────────

_gb_pipeline: Pipeline | None = None
_rf_pipeline: Pipeline | None = None
_feature_cols: list[str] = get_feature_columns()

FEATURE_LABELS = {
    "rainfall_mm":      "Rainfall Intensity",
    "aqi":              "Air Quality Index",
    "temperature_c":    "Temperature",
    "wind_speed":       "Wind Speed",
    "season_factor":    "Seasonal Risk Factor",
    "city_encoded":     "City Risk Profile",
    "platform_density": "Platform Delivery Density",
    "disruption_rate":  "Historical Disruption Rate",
    "platform_score":   "Platform Activity Score",
    "weekly_income":    "Income Exposure",
    "month":            "Month",
}


def _train_models():
    global _gb_pipeline, _rf_pipeline

    df = generate_training_data(n_per_city=800, seed=42)
    X = df[_feature_cols].values
    y = df["risk_score"].values

    _gb_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            random_state=42,
        )),
    ])
    _gb_pipeline.fit(X, y)

    _rf_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(
            n_estimators=150,
            max_depth=6,
            random_state=42,
            n_jobs=-1,
        )),
    ])
    _rf_pipeline.fit(X, y)


def _get_models():
    global _gb_pipeline, _rf_pipeline
    if _gb_pipeline is None:
        _train_models()
    return _gb_pipeline, _rf_pipeline


def _build_feature_vector(city: str, platform: str, weekly_income: int, month: int) -> np.ndarray:
    city_list = list(CITY_PROFILES.keys())
    city_idx = city_list.index(city) if city in city_list else 0
    p = get_city_profile(city)
    sf = SEASON_ENCODE.get(month, 0.5)
    pf = PLATFORM_ENCODE.get(platform, 0.7)

    # Use mean profile values as the "current snapshot"
    return np.array([[
        city_idx,                   # city_encoded
        month,                      # month
        sf,                         # season_factor
        p["rainfall_mm"][0] * sf,  # rainfall_mm (season-adjusted mean)
        p["aqi"][0],                # aqi
        p["temperature_c"][0],      # temperature_c
        p["wind_speed"][0],         # wind_speed
        weekly_income,              # weekly_income
        pf,                         # platform_score
        p["disruption_rate"],       # disruption_rate
        p["platform_density"],      # platform_density
    ]])


def compute_risk(city: str, platform: str, weekly_income: int, month: int) -> dict:
    """
    Main entry point.  Returns:
      risk_score, risk_label, confidence_interval,
      feature_importances, disruption_prob, model_used
    """
    gb, rf = _get_models()
    X = _build_feature_vector(city, platform, weekly_income, month)

    gb_score = float(np.clip(gb.predict(X)[0], 0, 1))
    rf_score = float(np.clip(rf.predict(X)[0], 0, 1))

    # Ensemble: weighted average (GB slightly more weight)
    risk_score = round(0.6 * gb_score + 0.4 * rf_score, 4)

    # Confidence interval from RF tree variance
    rf_model = rf.named_steps["model"]
    tree_preds = np.array([t.predict(rf.named_steps["scaler"].transform(X))[0]
                           for t in rf_model.estimators_])
    ci_low  = float(np.clip(np.percentile(tree_preds, 10), 0, 1))
    ci_high = float(np.clip(np.percentile(tree_preds, 90), 0, 1))

    # Risk label
    if risk_score >= 0.65:
        risk_label = "High"
    elif risk_score >= 0.40:
        risk_label = "Medium"
    else:
        risk_label = "Low"

    # Feature importances from GB model
    gb_model = gb.named_steps["model"]
    importances = gb_model.feature_importances_
    feature_importances = []
    for feat, imp in zip(_feature_cols, importances):
        feature_importances.append({
            "feature":      FEATURE_LABELS.get(feat, feat),
            "importance":   round(float(imp), 4),
            "contribution": round(float(imp) * risk_score, 4),
        })
    feature_importances.sort(key=lambda x: x["importance"], reverse=True)

    # Disruption probability: logistic transform of risk score
    disruption_prob = round(1 / (1 + np.exp(-8 * (risk_score - 0.45))), 4)

    return {
        "city":                city,
        "risk_score":          risk_score,
        "risk_label":          risk_label,
        "confidence_interval": (round(ci_low, 4), round(ci_high, 4)),
        "feature_importances": feature_importances,
        "disruption_prob":     float(disruption_prob),
        "model_used":          "GradientBoosting + RandomForest Ensemble",
    }
