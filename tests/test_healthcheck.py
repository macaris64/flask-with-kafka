import pytest
from flask import current_app

from app.app import app

def test_healthcheck():
    test_client = app.test_client()

    response = test_client.get('/healthcheck')
    assert response.status_code == 200
    assert response.json == {
        "status": "healthy",
        "kafka_producer_initialized": False,
    }
