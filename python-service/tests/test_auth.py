"""Tests for authentication endpoints."""
import json
import pytest


class TestRegistration:
    """Tests for POST /api/auth/register."""

    def test_register_success(self, client):
        """Should register a new user successfully."""
        response = client.post(
            "/api/auth/register",
            data=json.dumps({
                "email": "newuser@example.com",
                "password": "securepassword123",
                "name": "New User",
            }),
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["user"]["email"] == "newuser@example.com"
        assert "access_token" in data

    def test_register_missing_fields(self, client):
        """Should return 400 when required fields are missing."""
        response = client.post(
            "/api/auth/register",
            data=json.dumps({"email": "user@example.com"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_register_duplicate_email(self, client, sample_user):
        """Should return 409 when email is already registered."""
        response = client.post(
            "/api/auth/register",
            data=json.dumps({
                "email": "test@example.com",  # Same as sample_user
                "password": "password123",
                "name": "Duplicate User",
            }),
            content_type="application/json",
        )
        assert response.status_code == 409


class TestLogin:
    """Tests for POST /api/auth/login."""

    def test_login_success(self, client, sample_user):
        """Should return JWT token for valid credentials."""
        response = client.post(
            "/api/auth/login",
            data=json.dumps({
                "email": "test@example.com",
                "password": "testpassword123",
            }),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"

    def test_login_wrong_password(self, client, sample_user):
        """Should return 401 for incorrect password."""
        response = client.post(
            "/api/auth/login",
            data=json.dumps({
                "email": "test@example.com",
                "password": "wrongpassword",
            }),
            content_type="application/json",
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Should return 401 for non-existent email."""
        response = client.post(
            "/api/auth/login",
            data=json.dumps({
                "email": "nonexistent@example.com",
                "password": "password123",
            }),
            content_type="application/json",
        )
        assert response.status_code == 401

    def test_login_missing_fields(self, client):
        """Should return 400 when email or password is missing."""
        response = client.post(
            "/api/auth/login",
            data=json.dumps({"email": "test@example.com"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_login_bytes_password_hash(self, client, sample_user):
        """Should handle bytes-like password_hash without TypeError (DEV-141 fix)."""
        # Ensure the sample_user's password_hash is a bytes-like object (as stored in DB)
        from app.models.user import User
        user = User.query.filter_by(email="test@example.com").first()
        assert isinstance(user.password_hash, str)  # Stored as string in DB, but encoded to bytes for bcrypt
        
        # Attempt login (should not raise TypeError)
        response = client.post(
            "/api/auth/login",
            data=json.dumps({
                "email": "test@example.com",
                "password": "testpassword123",
            }),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert "access_token" in response.get_json()
