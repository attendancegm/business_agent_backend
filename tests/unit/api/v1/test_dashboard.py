def test_get_dashboard_overview_empty_db(client):
    response = client.get("/api/v1/dashboard/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["pending_approvals"] == 0
    assert data["active_tasks"] == {}
    assert isinstance(data["content_scheduled_today"], list)

def test_get_metrics(client):
    response = client.get("/api/v1/dashboard/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "content_metrics" in data
    assert "communication_metrics" in data
    # Ensure no division by zero caused issues by checking values exist
    assert data["content_metrics"]["total_posts"] == 0
