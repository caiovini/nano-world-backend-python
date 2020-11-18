
import main
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

"""
    Integration tests
    Make sure nano node is up

"""


@pytest.fixture
def app():
    app = main.app
    yield app
    app.container.unwire()
    

def test_get_peers(app : FastAPI) -> None:

    client = TestClient(app)
    client.headers["Content-Type"] = "application/json"
    response = client.get("/getPeers")
        
    assert response.status_code == 200

def test_get_geo_locations(app : FastAPI) -> None:

    client = TestClient(app)
    client.headers["Content-Type"] = "application/json"
    response = client.get("/getGeoLocations")
        
    assert response.status_code == 200

def test_get_balance(app : FastAPI) -> None:

    client = TestClient(app)
    client.headers["Content-Type"] = "application/json"
    response = client.get("/getBalance/xrb_1111111111111111111111111111111111111111111111111111hifc8npp")
        
    assert response.status_code == 200


    