"""Test suite for Clau Financial Advisory Chatbot Backend

This module contains comprehensive tests for the FastAPI backend service,
including API endpoint validation, error handling, and integration testing
with mocked external services.
"""

import pytest
from fastapi.testclient import TestClient
from main import app
import httpx  # Import httpx for proper mocking

# Initialize test client for API testing
client = TestClient(app)

def test_root():
    """Test health check endpoint functionality
    
    Verifies that the root endpoint returns proper status and message,
    which is essential for monitoring and deployment verification.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json().get("message", "").lower()

def test_ask_success(monkeypatch):
    """Test successful financial advice request with mocked Gemini API
    
    This test verifies the complete request flow using monkeypatch to mock
    the external API call for reliable testing.
    """
    # This is the correct way to mock the client used by TestClient
    def mock_post(url, json=None, headers=None):
        # Simulate Gemini's nested response structure
        mock_response_data = {
            "candidates": [
                {"content": {"parts": [{"text": "Budget 50/30/20 rule\n\n**Final Recommendation: Save 20% of income**"}]}}
            ]
        }
        return httpx.Response(status_code=200, json=mock_response_data)

    # Replace httpx.post with our mock for this test
    monkeypatch.setattr(httpx, "post", mock_post)
    
    # Test with typical financial question
    response = client.post("/ask", json={
        "contents": [
            {
                "role": "user",
                "parts": [{"text": "How should I budget?"}]
            }
        ]
    })
    
    # Verify successful response with expected format
    assert response.status_code == 200
    assert "Final Recommendation" in response.json()["answer"]

def test_ask_missing_api_key(monkeypatch):
    """Test error handling when Gemini API key is not configured
    
    This test ensures the application fails gracefully when the required
    API key is missing. This test is expected to pass by asserting the failure.
    """
    # Simulate missing API key scenario by setting it to an empty string
    monkeypatch.setenv("GEMINI_API_KEY", "")
    
    # This mock will simulate an auth error from the real API
    def mock_post_auth_error(url, json=None, headers=None):
        error_response = {
            "error": {
                "code": 401,
                "message": "API key not valid. Please pass a valid API key.",
                "status": "UNAUTHENTICATED"
            }
        }
        return httpx.Response(status_code=401, json=error_response)

    monkeypatch.setattr(httpx, "post", mock_post_auth_error)

    response = client.post("/ask", json={
        "contents": [{"role": "user", "parts": [{"text": "test"}]}]
    })
    
    # The application should catch the error and return a 500 status
    assert response.status_code == 500
    assert "API key not valid" in response.json()["detail"]

def test_ask_invalid_payload():
    """Test request validation with malformed payload
    
    Verifies that Pydantic validation properly rejects invalid requests,
    which is crucial for API security and data integrity.
    """
    # Send request with invalid structure
    response = client.post("/ask", json={"invalid": "data"})
    # Should return 422 Unprocessable Entity for validation errors
    assert response.status_code == 422
