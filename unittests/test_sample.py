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
    def __init__(self, table_data=None):
        self.auth = MockAuth()
        self.last_table_name = None
        self.last_table = None
        self.table_data = table_data if table_data is not None else [{"plant": "Monstera"}]

    def table(self, name):
       self.last_table_name = name
       self.last_table = MockTable(self.table_data)
       return self.last_table


# =========================
# Fixture (ska ligga på modulnivå, inte inuti klass)
# =========================
@pytest.fixture(autouse=True)
def mock_supabase_client(mocker):
    mock_client = MockSupabaseClient()
    # Ersätter global supabaseClient i databaseConnection
    mocker.patch.object(databaseConnection, "get_client_for_token", mock_client)
    mocker.patch.object(databaseConnection, "get_admin_client", mock_client)
    return mock_client


# =========================
# Tester
# =========================
def test_get_user_plants_returns_data(mock_supabase_client):
    result = databaseConnection.getUserPlants("user123", token="tkn", client=mock_supabase_client)
    assert isinstance(result, list)
    assert result[0]["plant"] == "Monstera"


def test_delete_user_plant_returns_deleted_data(mock_supabase_client):
    result = databaseConnection.deleteUserPlant(1, "user123", token="tkn", client=mock_supabase_client)
    assert result[0][0]["plant"] == "Monstera"


def test_register_user_returns_success(mock_supabase_client):
    result = databaseConnection.registerUser("a@b.com", "password", client=mock_supabase_client)
    assert result == "success"


def test_sign_out_user_returns_success(mock_supabase_client):
    result = databaseConnection.signOutUser(token="tkn", client=mock_supabase_client)
    assert result == "success"


def test_change_password_returns_success(mock_supabase_client):
    result = databaseConnection.changePassword(access_token="tkn", new_password="newpassword", client=mock_supabase_client)
    assert result == "success"
