"""
tests/test_anomaly_detector.py
Tests for the Isolation Forest trigger detector.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from models.anomaly_detector import check_triggers, ALERT_THRESHOLDS


class TestAnomalyDetector:
    """Tests that the Isolation Forest correctly detects anomalous conditions."""

    def test_returns_four_triggers(self):
        result = check_triggers("Bangalore")
        assert len(result["triggers"]) == 4

    def test_all_trigger_names_present(self):
        result  = check_triggers("Delhi")
        names   = {t["name"] for t in result["triggers"]}
        assert names == {"Rainfall", "AQI", "Heat", "Wind"}

    def test_trigger_statuses_valid(self):
        result = check_triggers("Mumbai")
        valid  = {"normal", "warning", "alert"}
        for t in result["triggers"]:
            assert t["status"] in valid

    def test_anomaly_score_bounded(self):
        result = check_triggers("Hyderabad")
        for t in result["triggers"]:
            assert 0.0 <= t["anomaly_score"] <= 1.0

    def test_extreme_rainfall_triggers_alert(self):
        """Injecting 100mm rainfall should trigger an alert for any city."""
        conditions = {
            "rainfall_mm":   100.0,
            "aqi":           80.0,
            "temperature_c": 28.0,
            "wind_speed":    12.0,
        }
        result   = check_triggers("Bangalore", current_conditions=conditions)
        rainfall = next(t for t in result["triggers"] if t["name"] == "Rainfall")
        assert rainfall["status"] == "alert"
        assert result["any_alert"] is True

    def test_extreme_aqi_triggers_alert(self):
        conditions = {
            "rainfall_mm":   5.0,
            "aqi":           300.0,
            "temperature_c": 28.0,
            "wind_speed":    10.0,
        }
        result = check_triggers("Delhi", current_conditions=conditions)
        aqi_t  = next(t for t in result["triggers"] if t["name"] == "AQI")
        assert aqi_t["status"] == "alert"

    def test_normal_conditions_no_alert(self):
        """Typical calm conditions should produce no alerts."""
        conditions = {
            "rainfall_mm":   3.0,
            "aqi":           60.0,
            "temperature_c": 26.0,
            "wind_speed":    8.0,
        }
        result = check_triggers("Hyderabad", current_conditions=conditions)
        assert result["any_alert"] is False

    def test_any_alert_flag_consistent(self):
        result    = check_triggers("Chennai")
        has_alert = any(t["status"] == "alert" for t in result["triggers"])
        assert result["any_alert"] == has_alert

    def test_model_used_field(self):
        result = check_triggers("Bangalore")
        assert "IsolationForest" in result["model_used"]
