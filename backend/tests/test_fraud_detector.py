"""
tests/test_fraud_detector.py
Tests for the multi-signal OC-SVM fraud detection engine.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from models.fraud_detector import evaluate_fraud

# Clean legitimate signals (all signals strongly pass)
CLEAN_SIGNALS = {
    "gps":     0.95,
    "motion":  0.88,
    "network": 0.80,
    "platform":0.92,
    "device":  0.97,
    "cluster": 0.05,   # low cluster risk = good
}

# Clearly fraudulent (GPS spoofed, no platform activity, cluster ring)
FRAUD_SIGNALS = {
    "gps":     0.10,
    "motion":  0.08,
    "network": 0.20,
    "platform":0.12,
    "device":  0.25,
    "cluster": 0.90,   # high cluster risk = suspicious
}

# Ambiguous (some signals pass, some marginal)
AMBIGUOUS_SIGNALS = {
    "gps":     0.55,
    "motion":  0.60,
    "network": 0.50,
    "platform":0.65,
    "device":  0.88,
    "cluster": 0.30,
}


class TestFraudDetector:

    def test_clean_signals_green_tier(self):
        result = evaluate_fraud("w001", "Bangalore", 80.0, CLEAN_SIGNALS, 700)
        assert result["tier"] == "green", f"Expected green, got {result['tier']}"

    def test_fraud_signals_red_tier(self):
        result = evaluate_fraud("w002", "Delhi", 20.0, FRAUD_SIGNALS, 700)
        assert result["tier"] in ("yellow", "red"), f"Expected red/yellow, got {result['tier']}"

    def test_fraud_score_bounded(self):
        for signals in [CLEAN_SIGNALS, FRAUD_SIGNALS, AMBIGUOUS_SIGNALS]:
            result = evaluate_fraud("w003", "Mumbai", 50.0, signals, 500)
            assert 0.0 <= result["fraud_score"] <= 1.0

    def test_clean_lower_fraud_score_than_fraud(self):
        clean = evaluate_fraud("w004", "Bangalore", 50.0, CLEAN_SIGNALS, 700)["fraud_score"]
        fraud = evaluate_fraud("w005", "Bangalore", 50.0, FRAUD_SIGNALS, 700)["fraud_score"]
        assert clean < fraud, f"Clean ({clean}) should be less fraudulent than fraud ({fraud})"

    def test_six_signals_returned(self):
        result = evaluate_fraud("w006", "Chennai", 60.0, CLEAN_SIGNALS, 1000)
        assert len(result["signals"]) == 6

    def test_each_signal_has_required_fields(self):
        result = evaluate_fraud("w007", "Hyderabad", 70.0, CLEAN_SIGNALS, 500)
        for sig in result["signals"]:
            assert "key" in sig
            assert "label" in sig
            assert "confidence" in sig
            assert "passed" in sig
            assert "weight" in sig
            assert "explanation" in sig

    def test_high_trust_score_benefits_legit_worker(self):
        """High trust score should slightly reduce fraud score for borderline case."""
        low_trust  = evaluate_fraud("w008", "Mumbai", 10.0, AMBIGUOUS_SIGNALS, 700)["fraud_score"]
        high_trust = evaluate_fraud("w009", "Mumbai", 90.0, AMBIGUOUS_SIGNALS, 700)["fraud_score"]
        assert high_trust <= low_trust, "High trust worker should have <= fraud score than low trust"

    def test_large_claim_raises_scrutiny(self):
        """A claim over ₹1500 should have a slightly higher fraud score."""
        small = evaluate_fraud("w010", "Bangalore", 50.0, AMBIGUOUS_SIGNALS, 500)["fraud_score"]
        large = evaluate_fraud("w011", "Bangalore", 50.0, AMBIGUOUS_SIGNALS, 2500)["fraud_score"]
        assert large >= small

    def test_confidence_bounded(self):
        result = evaluate_fraud("w012", "Delhi", 50.0, CLEAN_SIGNALS, 700)
        assert 0.0 <= result["confidence"] <= 1.0

    def test_recommended_action_present(self):
        result = evaluate_fraud("w013", "Bangalore", 50.0, CLEAN_SIGNALS, 700)
        assert len(result["recommended_action"]) > 0
