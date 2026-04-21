from fastapi.testclient import TestClient
from unittest.mock import patch
from src.server import app

client = TestClient(app)


def test_add_plant_endpoint_exists():
    # fake logged-in user
    fake_user = type(
        "UserWrapper",
        (),
        {"user": type("User", (), {"id": 1})()}
    )()

    with patch("src.server.app.get_current_user_from_cookie", return_value=None), \
         patch("src.server.app.add_plant", return_value=[]):

        response = client.post(
            "/myPlants/addPlant",
            json={
                "plant_id": 123,
                "common_name": "Basil"
            }
        )

    assert response.status_code == 200
    assert response.json()["error"] == "NOT_LOGGED_IN"


def test_add_plant_rejects_wrong_types():
    fake_user = type(
        "UserWrapper",
        (),
        {"user": type("User", (), {"id": 1})()}
    )()

    with patch("src.server.app.get_current_user_from_cookie", return_value=fake_user):
        response = client.post(
            "/myPlants/addPlant",
            json={
                "plant_id": "not-an-int",
                "common_name": 123
            }
        )

    # FastAPI + Pydantic should reject this automatically
    assert response.status_code == 422