import pytest
from datetime import date

from src.server.database import databaseConnection

# =========================
# Mock-klasser
# =========================
class MockResponse:
    def __init__(self, data=None, session=None):
        self.data = data
        self.session = session


class MockTable:
    def __init__(self, data):
        self.data = data
        self.calls = []
        self.insert_payload = None

    def delete(self):
        self.calls.append(("delete", args))
        return self

    def select(self, *args):
        self.calls.append(("select", args))
        return self

    def insert(self, payload):
        self.calls.append(("insert", payload))
        self.insert_payload = payload
        return self

    def eq(self, column, value):
        self.calls.append(("eq", column, value))
        return self

    def execute(self):
        self.calls.append(("execute",))
        return MockResponse(data=self.data)


class MockAuth:
    def __init__(self):
        self.calls = []
        self.raise_on = set()
        self.login_session_value = "session_token_123"

    def sign_up(self, payload):
        self.calls.append(("sign_up", payload))
        if "sign_up" in self.raise_on:
            raise Expection("User already exists")
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