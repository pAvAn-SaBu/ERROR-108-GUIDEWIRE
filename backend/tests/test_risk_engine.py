"""
tests/test_risk_engine.py
Tests for the Risk Prediction Engine (GB + RF ensemble).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from models.risk_engine import compute_risk


class TestRiskEngine:
    """Tests that the GB+RF ensemble produces sensible risk scores."""

    def test_delhi_higher_risk_than_hyderabad(self):
        delhi_risk = compute_risk("Delhi",     "Swiggy", 6000, 7)["risk_score"]
        hyd_risk   = compute_risk("Hyderabad", "Swiggy", 6000, 7)["risk_score"]
        assert delhi_risk > hyd_risk, (
            f"Delhi ({delhi_risk}) should have higher risk than Hyderabad ({hyd_risk})"
        )

    def test_mumbai_higher_risk_than_chennai(self):
        mum = compute_risk("Mumbai",  "Zomato", 6000, 7)["risk_score"]
        chn = compute_risk("Chennai", "Zomato", 6000, 7)["risk_score"]
        assert mum > chn

    def test_monsoon_higher_risk_than_winter(self):
        monsoon = compute_risk("Bangalore", "Swiggy", 6000, month=7)["risk_score"]
        winter  = compute_risk("Bangalore", "Swiggy", 6000, month=12)["risk_score"]
        assert monsoon > winter, "Monsoon month should have higher risk than winter"

    def test_risk_score_bounded(self):
        for city in ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad"]:
            score = compute_risk(city, "Swiggy", 6000, 7)["risk_score"]
            assert 0.0 <= score <= 1.0, f"Risk score out of bounds for {city}: {score}"

    def test_risk_labels_correct(self):
        high   = compute_risk("Delhi",     "Swiggy", 6000, 7)
        low    = compute_risk("Hyderabad", "Swiggy", 6000, 1)
        assert high["risk_label"] in ("Medium", "High")
        assert low["risk_label"]  in ("Low", "Medium")

    def test_feature_importances_sum_to_one(self):
        result = compute_risk("Bangalore", "Swiggy", 6000, 6)
        total  = sum(f["importance"] for f in result["feature_importances"])
        assert abs(total - 1.0) < 1e-4, f"Feature importances don't sum to 1: {total}"

    def test_confidence_interval_valid(self):
        result = compute_risk("Mumbai", "Zomato", 8000, 8)
        ci_low, ci_high = result["confidence_interval"]
        assert 0 <= ci_low <= ci_high <= 1

    def test_disruption_prob_bounded(self):
        result = compute_risk("Delhi", "Swiggy", 6000, 7)
        assert 0.0 <= result["disruption_prob"] <= 1.0

    def test_model_name_in_response(self):
        result = compute_risk("Bangalore", "Swiggy", 6000, 5)
        assert "GradientBoosting" in result["model_used"]
