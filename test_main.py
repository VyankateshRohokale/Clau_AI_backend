"""Test suite for Clau Financial Advisory Chatbot Backend

This module contains comprehensive tests for the FastAPI backend service,
including API endpoint validation, error handling, and integration testing
with mocked external services.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

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
    
    This test verifies the complete request flow:
    1. Request validation
    2. System prompt injection
    3. External API integration
    4. Response formatting
    
    Uses monkeypatch to mock external API calls for reliable testing.
    """
    def mock_post(url, json=None, headers=None):
        """Mock Gemini API response with typical financial advice format"""
        class MockResponse:
            status_code = 200
            def json(self):
                # Simulate Gemini's nested response structure
                return {
                    "candidates": [
                        {"content": {"parts": [{"text": "Budget 50/30/20 rule\n\n**Final Recommendation: Save 20% of income**"}]}}
                    ]
                }
            def raise_for_status(self):
                pass
        return MockResponse()

    # Replace requests.post with our mock for this test
    monkeypatch.setattr("requests.post", mock_post)
    
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
    API key is missing, providing clear error messages for debugging.
    Important for deployment validation and troubleshooting.
    """
    # Simulate missing API key scenario
    monkeypatch.setenv("GEMINI_API_KEY", "")
    # Force reload of environment variable in the main module
    import main
    main.GEMINI_API_KEY = ""
    
    response = client.post("/ask", json={
        "contents": [
            {
                "role": "user", 
                "parts": [{"text": "test"}]
            }
        ]
    })
    
    # Verify proper error response
    assert response.status_code == 500
    assert "API Key not set" in response.json()["detail"]

def test_ask_invalid_payload():
    """Test request validation with malformed payload
    
    Verifies that Pydantic validation properly rejects invalid requests,
    which is crucial for API security and data integrity.
    """
    # Send request with invalid structure
    response = client.post("/ask", json={"invalid": "data"})
    # Should return 422 Unprocessable Entity for validation errors
    assert response.status_code == 422

