from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_unregister_participant_removes_email():
    original_participants = list(activities["Chess Club"]["participants"])

    try:
        response = client.delete(
            "/activities/Chess%20Club/participants/michael@mergington.edu"
        )

        assert response.status_code == 200
        assert response.json()["message"].startswith("Removed michael@mergington.edu")

        updated_activities = client.get("/activities").json()
        assert "michael@mergington.edu" not in updated_activities["Chess Club"]["participants"]
    finally:
        activities["Chess Club"]["participants"] = original_participants


def test_unregister_participant_returns_404_for_unknown_email():
    response = client.delete(
        "/activities/Chess%20Club/participants/unknown@mergington.edu"
    )

    assert response.status_code == 404
