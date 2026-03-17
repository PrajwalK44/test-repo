"""
Test cases for the custom JSON encoder fix.

This module validates that the custom JSON encoder correctly serializes:
- datetime and date objects
- Decimal objects
- Flask app startup and JSON encoder registration
- Edge cases (invalid inputs, nested objects)
"""

import pytest
from datetime import datetime, date
from decimal import Decimal
from flask import Flask, jsonify
from app import create_app, CustomJSONEncoder


@pytest.fixture
def app():
    """Create a test Flask app with the custom JSON encoder."""
    app = create_app("testing")
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


def test_custom_json_encoder_serializes_datetime():
    """Test that the custom JSON encoder correctly serializes datetime objects."""
    encoder = CustomJSONEncoder()
    now = datetime.now()
    result = encoder.default(now)
    assert result == now.isoformat()


def test_custom_json_encoder_serializes_date():
    """Test that the custom JSON encoder correctly serializes date objects."""
    encoder = CustomJSONEncoder()
    today = date.today()
    result = encoder.default(today)
    assert result == today.isoformat()


def test_custom_json_encoder_serializes_decimal():
    """Test that the custom JSON encoder correctly serializes Decimal objects."""
    encoder = CustomJSONEncoder()
    decimal_value = Decimal("123.45")
    result = encoder.default(decimal_value)
    assert result == 123.45


def test_custom_json_encoder_falls_back_to_default():
    """Test that the custom JSON encoder falls back to the default behavior for unsupported types."""
    encoder = CustomJSONEncoder()
    with pytest.raises(TypeError):
        encoder.default(object())


def test_flask_app_uses_custom_json_encoder(app):
    """Test that the Flask app uses the custom JSON encoder."""
    assert isinstance(app.json_provider_class(), CustomJSONEncoder)


def test_flask_app_serializes_datetime_in_response(client):
    """Test that the Flask app correctly serializes datetime objects in responses."""
    @client.application.route("/test-datetime")
    def test_route():
        return jsonify({"now": datetime.now()})

    response = client.get("/test-datetime")
    assert response.status_code == 200
    data = response.get_json()
    assert "now" in data
    assert isinstance(data["now"], str)


def test_flask_app_serializes_decimal_in_response(client):
    """Test that the Flask app correctly serializes Decimal objects in responses."""
    @client.application.route("/test-decimal")
    def test_route():
        return jsonify({"price": Decimal("123.45")})

    response = client.get("/test-decimal")
    assert response.status_code == 200
    data = response.get_json()
    assert "price" in data
    assert data["price"] == "123.45"


def test_flask_app_serializes_nested_objects(client):
    """Test that the Flask app correctly serializes nested objects with datetime and Decimal."""
    @client.application.route("/test-nested")
    def test_route():
        return jsonify({
            "event": {
                "timestamp": datetime.now(),
                "value": Decimal("99.99")
            }
        })

    response = client.get("/test-nested")
    assert response.status_code == 200
    data = response.get_json()
    assert "event" in data
    assert isinstance(data["event"]["timestamp"], str)
    assert data["event"]["value"] == "99.99"