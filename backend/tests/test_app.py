
import pytest
import requests
from unittest.mock import patch, Mock
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# TEST 1: Backend connection
def test_home(client):
    response = client.get("/")

    assert response.status_code == 404
    assert response.json["message"] == "GitLost backend is running!"


# TEST 2: Invalid route
def test_invalid_route(client):
    response = client.get("/invalid")

    assert response.status_code == 404


# TEST 3: Missing API key
@patch("app.TICKETMASTER_API_KEY", None)
def test_missing_api_key(client):
    response = client.get("/api/events?city=Chicago")

    assert response.status_code == 500
    assert response.json["error"] == "API key not configured"