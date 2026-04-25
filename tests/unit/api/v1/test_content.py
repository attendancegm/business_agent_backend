import pytest
from unittest.mock import patch

def test_generate_content_invalid_payload(client):
    response = client.post(
        "/api/v1/content/generate",
        json={
            "platform": "twitter"
            # Missing "topic"
        }
    )
    assert response.status_code == 422

@patch("app.services.content_pipeline.ContentPipeline.evaluate_content")
@patch("app.services.openrouter_client.OpenRouterClient.generate_content_variations")
@patch("app.services.content_pipeline.ContentPipeline.create_content")
def test_generate_content_low_confidence(mock_create, mock_variations, mock_eval, client):
    mock_create.return_value = {
        "content_text": "Test",
        "platform": "twitter",
        "content_type": "social_post",
        "tone": "professional",
        "target_audience": "general"
    }
    mock_variations.return_value = ["Variation 1"]
    mock_eval.return_value = 0.5  # Low confidence

    response = client.post(
        "/api/v1/content/generate",
        json={
            "platform": "twitter",
            "topic": "AI",
            "content_type": "social_post",
            "tone": "professional",
            "target_audience": "general"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending_approval"

@patch("app.services.content_pipeline.ContentPipeline.evaluate_content")
@patch("app.services.openrouter_client.OpenRouterClient.generate_content_variations")
@patch("app.services.content_pipeline.ContentPipeline.create_content")
def test_generate_content_high_confidence(mock_create, mock_variations, mock_eval, client):
    mock_create.return_value = {
        "content_text": "Test",
        "platform": "twitter",
        "content_type": "social_post",
        "tone": "professional",
        "target_audience": "general"
    }
    mock_variations.return_value = ["Variation 1"]
    mock_eval.return_value = 0.96  # High confidence

    response = client.post(
        "/api/v1/content/generate",
        json={
            "platform": "twitter",
            "topic": "AI",
            "content_type": "social_post",
            "tone": "professional",
            "target_audience": "general"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
