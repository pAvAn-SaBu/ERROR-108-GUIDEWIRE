"""
tests/test_premium_engine.py
Tests for the dynamic premium calculator.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from models.premium_engine import calculate_premiums


class TestPremiumEngine:

    def test_three_plans_returned(self):
        result = calculate_premiums("Bangalore", 0.62, 6000)
        assert len(result["plans"]) == 3

    def test_high_risk_raises_premium(self):
        low  = calculate_premiums("Hyderabad", 0.36, 6000)
        high = calculate_premiums("Delhi",     0.80, 6000)
        for plan in ["basic", "standard", "premium"]:
            low_p  = next(p for p in low["plans"]  if p["plan"] == plan)["adjusted_premium"]
            high_p = next(p for p in high["plans"] if p["plan"] == plan)["adjusted_premium"]
            assert high_p > low_p, f"High risk {plan} should cost more than low risk"

    def test_low_risk_gets_discount(self):
        result = calculate_premiums("Hyderabad", 0.20, 3000)
        for plan in result["plans"]:
            assert plan["discount_pct"] < 0, "Low risk should get a premium discount"

    def test_high_risk_gets_surcharge(self):
        result = calculate_premiums("Delhi", 0.85, 8000)
        for plan in result["plans"]:
            assert plan["discount_pct"] > 0, "High risk should pay a surcharge"

    def test_coverage_matches_plan(self):
        result = calculate_premiums("Mumbai", 0.60, 6000)
        coverages = {p["plan"]: p["coverage"] for p in result["plans"]}
        assert coverages["basic"]    == 1000
        assert coverages["standard"] == 2000
        assert coverages["premium"]  == 3000

    def test_risk_adjustment_factor_sign(self):
        low  = calculate_premiums("Hyderabad", 0.30, 6000)
        high = calculate_premiums("Delhi",     0.80, 6000)
        assert low["risk_adjustment_factor"]  < 0
        assert high["risk_adjustment_factor"] > 0

    def test_premiums_are_positive(self):
        result = calculate_premiums("Chennai", 0.55, 5000)
        for plan in result["plans"]:
            assert plan["adjusted_premium"] > 0


class TestTrustEngine:
    """Basic trust score tests."""

    def test_trust_score_bounded(self):
        from models.trust_engine import compute_trust, update_trust
        update_trust("trust_test_1", True, False, 700)
        update_trust("trust_test_1", True, False, 700)
        result = compute_trust("trust_test_1")
        assert 0.0 <= result["score"] <= 100.0

    def test_false_flag_reduces_score(self):
        from models.trust_engine import compute_trust, update_trust, _worker_store
        _worker_store["clean_w"]  = {"total_claims": 5, "verified_claims": 5, "false_flags": 0, "total_payout": 3500, "account_days": 120}
        _worker_store["flagged_w"]= {"total_claims": 5, "verified_claims": 4, "false_flags": 2, "total_payout": 2800, "account_days": 120}
        clean   = compute_trust("clean_w")["score"]
        flagged = compute_trust("flagged_w")["score"]
        assert clean > flagged, "Clean worker should have higher trust than flagged worker"

    def test_tier_is_valid(self):
        from models.trust_engine import compute_trust
        result = compute_trust("any_worker")
        assert result["tier"] in ("bronze", "silver", "gold", "platinum")

    def test_trend_is_valid(self):
        from models.trust_engine import compute_trust
        result = compute_trust("any_worker")
        assert result["trend"] in ("improving", "stable", "declining")
