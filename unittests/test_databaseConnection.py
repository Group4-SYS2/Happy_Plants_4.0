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
            raise Exception("User already exists")
        return "ok"

    def sign_in_with_password(self, payload):
        self.calls.append(("sign_in_with_password", payload))
        if "sign_in_with_password" in self.raise_on:
            raise Exception("Invalid login")
        return MockResponse(session=self.login_session_value)

    def sign_out(self):
        self.calls.append(("sign_out",))
        if "sign_out" in self.raise_on:
            raise Exception("Auth sign out failed")
        return "ok"

    def update_user(self, payload):
        self.calls.append(("update_user", payload))
        if "update_user" in self.raise_on:
            raise Exception("Update failed")
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
# Fixtures
# =========================
@pytest.fixture
def mock_admin_client(mocker):
    client = MockSupabaseClient()
    mocker.patch.object(databaseConnection, "get_mock_admin_client", return_value=client)
    return client

@pytest.fixture
def mock_token_client(mocker):
    client = MockSupabaseClient()
    mocker.patch.object(databaseConnection, "get_client_for_token", return_value=client)
    return client

# =========================
# Tester: getUserPlants
# =========================
def test_get_user_plants_returns_data_and_filters_by_user(mock_token_client):
    result = databaseConnection.getUserPlants("user123", token="tkn")

    assert isinstance(result, list)
    assert result[0]["plant"] == "Monstera"

    assert mock_token_client.last_table_name == "user_plants"
    assert ("select", (("*",)) in mock_token_client.last_table.calls
    assert ("eq", "user_id", "user123") in mock_token_client.last_table.calls
    assert ("execute",) in mock_token_client.last_table.calls

def test_get_user_plants_returns_none_on_error(mocker):
    class ErrorClient(MockSupabaseClient):
        def table(self, name):
            t = super().table(name)

            def boom():
                raise Exception("DB down")

            t.execute = boom
            return t

    mocker.patch.object(databaseConnection, "get_client_for_token", return_value=ErrorClient())
    result = databaseConnection.getUserPlants("user123", token="tkn")
    assert result is None

# =========================
# Tester: deleteUserPlant
# =========================
def test_delete_user_plant_calls_delete_and_fillers(mock_token_client):
    result = databaseConnection.deleteUserPlant(plant_id=1, user_id="user123", token="tkn")

    assert result[0]["plant"] == "Monstera"
    assert mock_token_client.last_table_name == "user_plants"
    assert ("delete",) in mock_token_client.last_table.calls
    assert ("eq", "user_id", "user123") in mock_token_client.last_table.calls
    assert ("eq", "plant_id", 1) in mock_token_client.last_table.calls
    assert ("execute",) in mock_token_client.last_table.calls

def test_delete_user_plant_returns_none_on_error(mocker):
    class ErrorClient(MockSupabaseClient):
        def table(self, name):
            t = super().table(name)

            def boom():
                raise Exception("delete failed")

            t.execute = boom
            return t

    mocker.patch.object(databaseConnection, "get_client_for_token", return_value=ErrorClient())
    result = databaseConnection.deleteUserPlant(plant_id=1, user_id="user123", token="tkn")
    assert result is None

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