from app  import create_app
from app.extensions import api
import pytest

client = create_app()

def test_create_app():
    assert client is not None


def test_database_uri():
    assert client.config.get("SQLALCHEMY_DATABASE_URI") == "sqlite:///db.sqlite3"


def test_namespaces():
    assert len(api.namespaces) > 0


def test_namespaces_paths():
    assert any(ns.path == "/api/posts" for ns in api.namespaces)
    assert any(ns.path == "/api/comments" for ns in api.namespaces)

# Use pytest-cov to measure code coverage
@pytest.mark.parametrize("test_input, expected", [("config.py", True)])
def test_config_loading_with_param(test_input, expected):
    app = create_app()
    assert app.config.from_pyfile(test_input) == expected