"""
synthetic_data.py
-----------------
Generates realistic synthetic training data for Indian gig-economy cities.
Used to train the Risk Engine and Anomaly Detector.
"""

import numpy as np
import pandas as pd

# ── City-level environmental profiles ─────────────────────────────────────────
# Each city has: (mean_rainfall_mm, std_rainfall, mean_aqi, std_aqi,
#                 mean_temp_c, std_temp, mean_wind, std_wind,
#                 base_disruption_rate, platform_density)
CITY_PROFILES = {
    "Bangalore": {
        "rainfall_mm":      (8.5,  12.0),
        "aqi":              (95,   30.0),
        "temperature_c":    (26,    4.0),
        "wind_speed":       (12,    5.0),
        "disruption_rate":  0.22,
        "platform_density": 0.75,
        "base_risk":        0.58,
    },
    "Mumbai": {
        "rainfall_mm":      (18.0, 30.0),
        "aqi":              (120,  40.0),
        "temperature_c":    (30,    3.0),
        "wind_speed":       (18,    8.0),
        "disruption_rate":  0.35,
        "platform_density": 0.85,
        "base_risk":        0.74,
    },
    "Delhi": {
        "rainfall_mm":      (5.0,  10.0),
        "aqi":              (200,  80.0),
        "temperature_c":    (28,    9.0),
        "wind_speed":       (10,    4.0),
        "disruption_rate":  0.38,
        "platform_density": 0.90,
        "base_risk":        0.80,
    },
    "Chennai": {
        "rainfall_mm":      (12.0, 18.0),
        "aqi":              (85,   25.0),
        "temperature_c":    (32,    3.0),
        "wind_speed":       (14,    6.0),
        "disruption_rate":  0.25,
        "platform_density": 0.65,
        "base_risk":        0.52,
    },
    "Hyderabad": {
        "rainfall_mm":      (6.0,   8.0),
        "aqi":              (75,   20.0),
        "temperature_c":    (28,    5.0),
        "wind_speed":       (11,    4.0),
        "disruption_rate":  0.15,
        "platform_density": 0.60,
        "base_risk":        0.36,
    },
}

PLATFORM_ENCODE = {
    "Swiggy": 0.78,
    "Zomato": 0.80,
    "Blinkit": 0.72,
    "Zepto": 0.65,
    "Dunzo": 0.55,
}

SEASON_ENCODE = {
    1: 0.3, 2: 0.3, 3: 0.4,   # Winter/Spring
    4: 0.6, 5: 0.7, 6: 0.9,   # Summer / Pre-monsoon
    7: 1.0, 8: 1.0, 9: 0.85,  # Monsoon peak
    10: 0.5, 11: 0.4, 12: 0.35
}


def generate_training_data(n_per_city: int = 800, seed: int = 42) -> pd.DataFrame:
    """
    Generate n_per_city samples for each of the 5 cities.
    Returns a DataFrame with features and `risk_score` label.
    """
    rng = np.random.default_rng(seed)
    rows = []

    for city, p in CITY_PROFILES.items():
        for _ in range(n_per_city):
            month = rng.integers(1, 13)
            season_factor = SEASON_ENCODE[month]

            rainfall = max(0, rng.normal(*p["rainfall_mm"]) * season_factor)
            aqi = max(20, rng.normal(*p["aqi"]) * (0.8 + 0.4 * season_factor))
            temp = rng.normal(*p["temperature_c"])
            wind = max(0, rng.normal(*p["wind_speed"]))
            income = rng.integers(3000, 15000)
            platform_key = rng.choice(list(PLATFORM_ENCODE.keys()))
            platform_score = PLATFORM_ENCODE[platform_key]

            # Compute a realistic risk label (0–1)
            rain_contrib  = min(rainfall / 50.0, 1.0) * 0.30
            aqi_contrib   = min((aqi - 50) / 300.0, 1.0) * 0.25
            temp_contrib  = min(max(temp - 35, 0) / 15.0, 1.0) * 0.10
            season_contrib = season_factor * 0.15
            density_contrib = p["platform_density"] * 0.10
            base_contrib  = p["base_risk"] * 0.10
            noise = rng.normal(0, 0.04)

            risk_score = np.clip(
                rain_contrib + aqi_contrib + temp_contrib +
                season_contrib + density_contrib + base_contrib + noise,
                0.05, 0.97
            )

            rows.append({
                "city": city,
                "city_encoded": list(CITY_PROFILES.keys()).index(city),
                "month": month,
                "season_factor": season_factor,
                "rainfall_mm": round(rainfall, 2),
                "aqi": round(aqi, 1),
                "temperature_c": round(temp, 1),
                "wind_speed": round(wind, 1),
                "weekly_income": income,
                "platform_score": platform_score,
                "disruption_rate": p["disruption_rate"],
                "platform_density": p["platform_density"],
                "risk_score": round(float(risk_score), 4),
            })

    return pd.DataFrame(rows)


def generate_normal_weather(city: str, n: int = 500, seed: int = 99) -> pd.DataFrame:
    """
    Generate 'normal' weather samples for a city — used to train
    the Isolation Forest baseline (no extreme events).
    """
    rng = np.random.default_rng(seed)
    p = CITY_PROFILES[city]
    rows = []
    for _ in range(n):
        month = rng.integers(3, 11)  # avoid extreme months deliberately
        sf = SEASON_ENCODE[month]
        rows.append({
            "rainfall_mm":   max(0, rng.normal(p["rainfall_mm"][0] * 0.6, p["rainfall_mm"][1] * 0.5)),
            "aqi":           max(20, rng.normal(p["aqi"][0] * 0.8, p["aqi"][1] * 0.4)),
            "temperature_c": rng.normal(p["temperature_c"][0], p["temperature_c"][1] * 0.6),
            "wind_speed":    max(0, rng.normal(p["wind_speed"][0], p["wind_speed"][1] * 0.5)),
        })
    return pd.DataFrame(rows)


def get_feature_columns() -> list[str]:
    return [
        "city_encoded", "month", "season_factor",
        "rainfall_mm", "aqi", "temperature_c", "wind_speed",
        "weekly_income", "platform_score",
        "disruption_rate", "platform_density",
    ]


def get_city_profile(city: str) -> dict:
    return CITY_PROFILES.get(city, CITY_PROFILES["Bangalore"])
