import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json().get("message", "").lower()

def test_ask_success(monkeypatch):
    """Test successful ask endpoint with mocked Gemini response"""
    def mock_post(url, json=None, headers=None):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "candidates": [
                        {"content": {"parts": [{"text": "Budget 50/30/20 rule\n\n**Final Recommendation: Save 20% of income**"}]}}
                    ]
                }
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    
    response = client.post("/ask", json={
        "contents": [
            {
                "role": "user",
                "parts": [{"text": "How should I budget?"}]
            }
        ]
    })
    
    assert response.status_code == 200
    assert "Final Recommendation" in response.json()["answer"]

def test_ask_missing_api_key(monkeypatch):
    """Test ask endpoint when API key is missing"""
    monkeypatch.setenv("GEMINI_API_KEY", "")
    # Force reload of environment variable
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
    
    assert response.status_code == 500
    assert "API Key not set" in response.json()["detail"]

def test_ask_invalid_payload():
    """Test ask endpoint with invalid payload"""
    response = client.post("/ask", json={"invalid": "data"})
    assert response.status_code == 422

