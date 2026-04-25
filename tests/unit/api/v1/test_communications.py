import pytest

def test_create_follow_up_invalid_sequence(client):
    # Invalid sequence type falls back to standard
    response = client.post(
        "/api/v1/communications/follow-up",
        json={
            "contact_id": 1,
            "context": "Follow up on demo",
            "sequence_type": "invalid_type"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "follow_up" in data
    # Standard offsets are 0, 3, 7
    assert len(data["follow_up"]) == 3
    assert data["follow_up"][0]["sequence_type"] == "invalid_type"

def test_bulk_follow_up_empty_list(client):
    response = client.post(
        "/api/v1/communications/bulk-follow-up",
        json={
            "contact_ids": [],
            "context": "Webinar invite"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["total"] == 0
    assert data["result"]["items"] == []

def test_team_progress_empty(client):
    response = client.get("/api/v1/communications/team-progress")
    assert response.status_code == 200
    data = response.json()
    assert len(data["team_progress"]) == 1
    assert data["team_progress"][0]["team_member"] == "unassigned"
