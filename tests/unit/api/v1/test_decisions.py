import pytest
import json
from unittest.mock import patch

@patch("app.services.openrouter_client.OpenRouterClient.complete")
def test_analyze_decision_low_confidence(mock_complete, client):
    # Mock low confidence
    mock_complete.return_value = {
        "content": json.dumps({"recommendation": "Hold", "confidence": 0.5})
    }

    response = client.post(
        "/api/v1/decisions/analyze",
        json={
            "decision_type": "Pricing",
            "context": {"competitor_price": 50}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["requires_approval"] is True
    assert data["confidence_score"] == 0.5

@patch("app.services.openrouter_client.OpenRouterClient.complete")
def test_analyze_decision_high_confidence(mock_complete, client):
    # Mock high confidence
    mock_complete.return_value = {
        "content": json.dumps({"recommendation": "Launch", "confidence": 0.95})
    }

    response = client.post(
        "/api/v1/decisions/analyze",
        json={
            "decision_type": "Feature Prioritization",
            "context": {"requests": 100}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["requires_approval"] is False
    assert data["confidence_score"] == 0.95

@patch("app.services.openrouter_client.OpenRouterClient.complete")
def test_analyze_decision_fallback_on_fail(mock_complete, client):
    # Mock invalid JSON parsing
    mock_complete.return_value = {
        "content": "Not a JSON"
    }

    response = client.post(
        "/api/v1/decisions/analyze",
        json={
            "decision_type": "Urgent",
            "context": {}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["requires_approval"] is True
    assert data["confidence_score"] == 0.0
    assert data["ai_recommendation"] == "unknown"
