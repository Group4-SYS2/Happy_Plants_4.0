import pytest

from src.server.database import databaseConnection

# =========================
# Mock-klasser
# =========================
class MockResponse:
    def __init__(self, data):
        self.data = data


class MockTable:
    def __init__(self, data):
        self.data = data

    def delete(self):
        return self

    def select(self, *_):
        return self

    def eq(self, *_):
        return self

    def execute(self):
        return MockResponse(self.data)


class MockAuth:
    def sign_up(self, *_):
        return "ok"

    def sign_in_with_password(self, *_):
        return "ok"

    def sign_out(self):
        return "ok"

    def update_user(self, *_):
        return "ok"

    def get_user(self):
        return {"id": "user123"}


class MockSupabaseClient:
    def table(self, *_):
        # Returnerar "låtsas-tabell" med sampledata
        return MockTable([{"plant": "Monstera"}])

    auth = MockAuth()


# =========================
# Fixture (ska ligga på modulnivå, inte inuti klass)
# =========================
@pytest.fixture(autouse=True)
def mock_supabase_client(mocker):
    mock_client = MockSupabaseClient()
    # Ersätter global supabaseClient i databaseConnection
    mocker.patch.object(databaseConnection, "supabaseClient", mock_client)


# =========================
# Tester
# =========================
def test_get_user_plants_returns_data():
    result = databaseConnection.getUserPlants("user123")
    assert isinstance(result, list)
    assert result[0]["plant"] == "Monstera"


def test_delete_user_plant_returns_deleted_data():
    result = databaseConnection.deleteUserPlant(1, "user123")
    assert result[0]["plant"] == "Monstera"


def test_register_user_returns_success():
    result = databaseConnection.registerUser("a@b.com", "password")
    assert result == "success"


def test_login_user_returns_success():
    result = databaseConnection.loginUser("a@b.com", "password")
    assert result == "success"


def test_sign_out_user_returns_success():
    result = databaseConnection.signOutUser()
    assert result == "success"


def test_change_password_returns_success():
    result = databaseConnection.changePassword("newpassword")
    assert result == "success"