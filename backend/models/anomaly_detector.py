"""
models/anomaly_detector.py
--------------------------
Isolation Forest-based anomaly detector for environmental trigger events.
Trained on 'normal' weather baselines per city and detects when live
conditions are anomalous (heavy rain, AQI spike, heat wave, etc.)
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from data.synthetic_data import generate_normal_weather, get_city_profile, CITY_PROFILES, SEASON_ENCODE

# ── Trigger definitions ───────────────────────────────────────────────────────

TRIGGERS = [
    {
        "name":        "Rainfall",
        "feature":     "rainfall_mm",
        "unit":        "mm/day",
        "description": "Heavy rainfall reducing delivery viability",
    },
    {
        "name":        "AQI",
        "feature":     "aqi",
        "unit":        "AQI Index",
        "description": "Air quality hazardous for outdoor work",
    },
    {
        "name":        "Heat",
        "feature":     "temperature_c",
        "unit":        "°C",
        "description": "Extreme temperature unsafe for delivery workers",
    },
    {
        "name":        "Wind",
        "feature":     "wind_speed",
        "unit":        "km/h",
        "description": "High-speed winds causing road hazards",
    },
]

FEATURE_ORDER = ["rainfall_mm", "aqi", "temperature_c", "wind_speed"]

# Alert thresholds (physics-based, city-agnostic)
ALERT_THRESHOLDS = {
    "rainfall_mm":   {"warning": 25.0,  "alert": 50.0},
    "aqi":           {"warning": 150.0, "alert": 250.0},
    "temperature_c": {"warning": 38.0,  "alert": 43.0},
    "wind_speed":    {"warning": 40.0,  "alert": 65.0},
}

# Per-city trained models
_models: dict[str, dict] = {}


def _train_city(city: str):
    df = generate_normal_weather(city, n=600, seed=7)
    X = df[FEATURE_ORDER].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    iso = IsolationForest(
        n_estimators=200,
        contamination=0.05,   # expect 5% anomalies in normal data
        random_state=42,
        n_jobs=-1,
    )
    iso.fit(X_scaled)

    _models[city] = {"iso": iso, "scaler": scaler, "baseline_stats": {
        col: {"mean": float(df[col].mean()), "std": float(df[col].std())}
        for col in FEATURE_ORDER
    }}


def _get_model(city: str) -> dict:
    if city not in _models:
        _train_city(city)
    return _models[city]


def _simulate_current_conditions(city: str, seed: int | None = None) -> dict:
    """
    Simulate current weather reading for a city.
    Uses the city profile with realistic noise, occasionally injecting
    an extreme event to make demos interesting.
    """
    p = get_city_profile(city)
    rng = np.random.default_rng(seed)

    # ~20% chance of a notable weather event
    event_roll = rng.random()

    rainfall = max(0, rng.normal(*p["rainfall_mm"]))
    aqi      = max(20, rng.normal(*p["aqi"]))
    temp     = rng.normal(*p["temperature_c"])
    wind     = max(0, rng.normal(*p["wind_speed"]))

    if event_roll < 0.20:
        # inject extreme event — pick one randomly
        event_type = rng.choice(["rain", "aqi", "heat", "wind"])
        if event_type == "rain":
            rainfall = rng.uniform(55, 120)
        elif event_type == "aqi":
            aqi = rng.uniform(260, 400)
        elif event_type == "heat":
            temp = rng.uniform(41, 47)
        elif event_type == "wind":
            wind = rng.uniform(65, 100)

    return {
        "rainfall_mm":   round(rainfall, 2),
        "aqi":           round(aqi, 1),
        "temperature_c": round(temp, 1),
        "wind_speed":    round(wind, 1),
    }


def check_triggers(city: str, current_conditions: dict | None = None) -> dict:
    """
    Main entry point. Returns trigger statuses for a city.
    If current_conditions not provided, simulates live readings.
    """
    model_data = _get_model(city)
    iso     = model_data["iso"]
    scaler  = model_data["scaler"]

    # Use provided conditions or simulate
    if current_conditions is None:
        import time
        seed = int(time.time() // 300)  # changes every 5 minutes for demo feel
        conditions = _simulate_current_conditions(city, seed=seed)
    else:
        conditions = current_conditions

    # Score the full observation with Isolation Forest
    X = np.array([[conditions[f] for f in FEATURE_ORDER]])
    X_scaled = scaler.transform(X)
    # anomaly_score: negative = anomaly, score_samples returns raw scores
    raw_iso_score = iso.score_samples(X_scaled)[0]
    # Normalize to 0 (normal) → 1 (extreme anomaly)
    global_anomaly = float(np.clip(1 - (raw_iso_score + 0.5) / 1.0, 0, 1))

    results = []
    any_alert = False

    for trig in TRIGGERS:
        feat = trig["feature"]
        val  = conditions[feat]
        thresholds = ALERT_THRESHOLDS[feat]

        # Z-score vs trained baseline
        stats = model_data["baseline_stats"][feat]
        z = (val - stats["mean"]) / max(stats["std"], 0.01)
        # Per-feature anomaly score
        feat_anomaly = float(np.clip(abs(z) / 4.0, 0, 1))

        # Determine status
        if val >= thresholds["alert"]:
            status, label = "alert", "Alert"
            any_alert = True
        elif val >= thresholds["warning"] or feat_anomaly > 0.55:
            status, label = "warning", "Warning"
        else:
            status, label = "normal", "Normal"

        results.append({
            "name":          trig["name"],
            "status":        status,
            "label":         label,
            "anomaly_score": round(feat_anomaly, 4),
            "current_value": val,
            "unit":          trig["unit"],
            "threshold":     thresholds["alert"],
            "description":   trig["description"],
        })

    return {
        "city":       city,
        "triggers":   results,
        "any_alert":  any_alert,
        "model_used": "IsolationForest (per-city baseline)",
    }
