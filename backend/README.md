# Revo – ML Backend

> AI-powered parametric insurance engine for gig delivery workers.  
> **Branch:** `implementation` | **Stack:** Python 3.11 · FastAPI · scikit-learn · uvicorn

---

## Quick Start

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

- **Swagger UI:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc  
- **Health:** http://localhost:8000/health

---

## Architecture

```
backend/
├── main.py                    # FastAPI app + CORS
├── requirements.txt
├── pyproject.toml             # pytest config
├── .gitignore
│
├── data/
│   └── synthetic_data.py      # Training data generator (5 Indian cities)
│
├── models/                    # ML model implementations
│   ├── risk_engine.py         # Gradient Boosting + Random Forest ensemble
│   ├── anomaly_detector.py    # Isolation Forest (per-city baselines)
│   ├── fraud_detector.py      # One-Class SVM + 6-signal weighted ensemble
│   ├── premium_engine.py      # Risk-adjusted dynamic pricing
│   └── trust_engine.py        # Bayesian Beta-distribution trust scorer
│
├── schemas/
│   └── models.py              # Pydantic v2 request/response schemas
│
├── routers/
│   ├── risk.py                # POST /risk/score, POST /premium/calculate
│   ├── triggers.py            # GET  /triggers/{city}
│   ├── fraud.py               # POST /fraud/evaluate, GET/POST /trust/*
│   └── claims.py              # POST /claims/process  (full pipeline)
│
└── tests/
    ├── test_risk_engine.py
    ├── test_anomaly_detector.py
    ├── test_fraud_detector.py
    └── test_premium_engine.py
```

---

## API Reference

### Risk & Premium

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/risk/score` | ML risk score (GB + RF ensemble) |
| `POST` | `/premium/calculate` | Risk-adjusted weekly premiums |

**Example – Risk Score:**
```bash
curl -X POST http://localhost:8000/risk/score \
  -H "Content-Type: application/json" \
  -d '{"city":"Delhi","platform":"Swiggy","weekly_income":6000,"month":7}'
```
```json
{
  "city": "Delhi",
  "risk_score": 0.456,
  "risk_label": "Medium",
  "confidence_interval": [0.38, 0.52],
  "feature_importances": [
    {"feature": "Air Quality Index", "importance": 0.43, "contribution": 0.196},
    {"feature": "Rainfall Intensity", "importance": 0.36, "contribution": 0.164}
  ],
  "disruption_prob": 0.514,
  "model_used": "GradientBoosting + RandomForest Ensemble"
}
```

---

### Trigger Detection

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/triggers/{city}` | Isolation Forest anomaly scores for 4 triggers |

**Example:**
```bash
curl http://localhost:8000/triggers/Delhi
```
```json
{
  "city": "Delhi",
  "any_alert": true,
  "triggers": [
    {"name": "AQI", "status": "alert", "anomaly_score": 0.87,
     "current_value": 256.2, "threshold": 250.0, "unit": "AQI Index"}
  ],
  "model_used": "IsolationForest (per-city baseline)"
}
```

---

### Fraud Detection & Trust

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/fraud/evaluate` | 6-signal OC-SVM fraud scorer |
| `GET`  | `/trust/{worker_id}` | Bayesian trust score |
| `POST` | `/trust/update` | Update trust after claim outcome |

**Example – Fraud Evaluate:**
```bash
curl -X POST http://localhost:8000/fraud/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": "w001",
    "city": "Bangalore",
    "trust_score": 75,
    "claim_amount": 700,
    "signals": {
      "gps_consistency": 0.92,
      "motion_pattern": 0.85,
      "network_degradation": 0.78,
      "platform_activity": 0.90,
      "device_fingerprint": 0.96,
      "cluster_risk": 0.04
    }
  }'
```
```json
{
  "fraud_score": 0.12,
  "tier": "green",
  "confidence": 0.76,
  "explanation": "All signals consistent with genuine disruption. Payout approved.",
  "recommended_action": "Auto-approve payout via UPI"
}
```

---

### Full Claims Pipeline

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/claims/process` | Trigger → Risk → Fraud → Payout → Trust update |

This endpoint runs the **complete parametric claim pipeline** in one call:
1. Runs Isolation Forest trigger check — rejects if no active trigger
2. Computes GB+RF risk score
3. Runs 6-signal OC-SVM fraud evaluation
4. Decides payout amount (70% coverage on Alert, 40% on Warning)
5. Updates worker trust score via Bayesian update

---

## ML Models Detail

### Risk Engine — `GradientBoosting + RandomForest`
- Trained on 4,000 synthetic samples (800 per city × 5 cities)
- Features: `rainfall_mm`, `aqi`, `temperature_c`, `wind_speed`, `season_factor`, `city_profile`, `platform_density`, `disruption_rate`, `weekly_income`
- Output: risk score (0–1), feature importances, 80% confidence interval, disruption probability

### Anomaly Detector — `IsolationForest`
- One model per city, trained on 600 "normal" weather samples per city
- Contamination: 5% (tuned for rare extreme events)
- Scores each of 4 triggers: Rainfall, AQI, Heat, Wind
- Z-score + isolation score combined for robust anomaly detection

### Fraud Detector — `One-Class SVM + Ensemble`
- OC-SVM trained on 1,000 synthetic legitimate claim fingerprints
- 6 signals with learned weights: GPS (25%), Platform (25%), Motion (15%), Network (15%), Device (10%), Cluster (10%)
- Trust score bonus/penalty applied to final score
- Tier thresholds: Green < 0.28 | Yellow < 0.55 | Red ≥ 0.55

### Premium Engine — `Risk-Adjusted Pricing`
- Formula: `adjusted = base × (1 + 0.45 × (score − 0.50))` for high risk
- Discount formula: `base × (1 − 0.35 × (0.45 − score))` for low risk
- Income-based multiplier: 0.90× (low earners) → 1.20× (high earners)

### Trust Engine — `Bayesian Beta Distribution`
- Prior: Beta(1, 1) — uninformative start for new workers
- Updates on each verified or rejected claim
- Penalties: −8 points per false flag
- Bonuses: account age, payout history, clean record
- Tiers: Bronze → Silver → Gold → Platinum

---

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

Expected: **28 tests passing**

---

## City Risk Profiles (Training Baselines)

| City | Base Risk | Rainfall | AQI | Disruption Rate |
|------|-----------|----------|-----|-----------------|
| Delhi | 0.80 (High) | Low | Very High (200) | 38% |
| Mumbai | 0.74 (High) | High | High (120) | 35% |
| Bangalore | 0.58 (Medium) | Medium | Medium (95) | 22% |
| Chennai | 0.52 (Medium) | Medium | Low (85) | 25% |
| Hyderabad | 0.36 (Low) | Low | Low (75) | 15% |
