"""
main.py
-------
Revo – AI-Powered Parametric Insurance Backend
FastAPI application entry point.

Run with:
    cd backend
    uvicorn main:app --reload --port 8000

Swagger UI: http://localhost:8000/docs
Redoc:      http://localhost:8000/redoc
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.risk import router as risk_router, premium_router
from routers.triggers import router as triggers_router
from routers.fraud import router as fraud_router
from routers.claims import router as claims_router

# ── App ────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Revo – ML Backend",
    description="""
## Revo AI/ML Engine

Parametric insurance for gig delivery workers.  
All ML inference runs server-side using **scikit-learn** models trained on synthetic Indian city data.

### ML Models
| Endpoint | Model |
|----------|-------|
| `/risk/score` | Gradient Boosting + Random Forest ensemble |
| `/triggers/{city}` | Isolation Forest (per-city anomaly baseline) |
| `/fraud/evaluate` | One-Class SVM + weighted signal ensemble |
| `/premium/calculate` | Risk-adjusted pricing formula |
| `/claims/process` | Full parametric pipeline |
| `/trust/*` | Bayesian Beta-distribution trust scorer |
    """,
    version="1.0.0",
    contact={
        "name": "Revo Engineering",
        "url":  "https://github.com/pAvAn-SaBu/ERROR-108-GUIDEWIRE",
    },
    license_info={"name": "MIT"},
)

# ── CORS (allows the gigcare frontend at any origin) ───────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────

app.include_router(risk_router)
app.include_router(premium_router)
app.include_router(triggers_router)
app.include_router(fraud_router)
app.include_router(claims_router)


# ── Health check ───────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"], summary="Health check")
def health():
    return {"status": "ok", "service": "Revo ML Backend", "version": "1.0.0"}


@app.get("/", tags=["Health"], include_in_schema=False)
def root():
    return {
        "message": "Revo ML Backend is running.",
        "docs":    "/docs",
        "redoc":   "/redoc",
    }
