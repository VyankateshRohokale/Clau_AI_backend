# API Documentation

## Overview
The Clau Financial Advisory Chatbot Backend provides RESTful API endpoints for AI-powered financial advice using Google Gemini 2.5 Flash.

## Base URL
- **Production**: `https://clau-ai-backend.onrender.com`
- **Development**: `http://localhost:8000`

## Authentication
No authentication required for public endpoints.

## Endpoints

### Health Check
**GET** `/`

Returns the service status.

**Response:**
```json
{
  "message": "Financial Advisory Chatbot Backend is running"
}
```

**Status Codes:**
- `200 OK`: Service is running

---

### Ask Financial Question
**POST** `/ask`

Submit financial questions and receive AI-powered advice.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "How should I budget my monthly income of $5000?"
        }
      ]
    }
  ]
}
```

**Request Schema:**
- `contents` (array): Array of message objects
  - `role` (string): Message sender role (`"user"` or `"model"`)
  - `parts` (array): Array of message parts
    - `text` (string): The message content

**Response:**
```json
{
  "answer": "To budget your $5000 monthly income effectively, follow the 50/30/20 rule:\n\n**Needs (50% - $2500):**\n- Rent/mortgage\n- Utilities\n- Groceries\n- Transportation\n- Insurance\n\n**Wants (30% - $1500):**\n- Entertainment\n- Dining out\n- Hobbies\n- Non-essential shopping\n\n**Savings (20% - $1000):**\n- Emergency fund\n- Retirement contributions\n- Investment accounts\n\n**Final Recommendation: Allocate $2500 for needs, $1500 for wants, and save $1000 monthly.**"
}
```

**Status Codes:**
- `200 OK`: Successful response
- `500 Internal Server Error`: API key missing or Gemini API error

**Error Response:**
```json
{
  "detail": "Gemini API Key not set"
}
```

## Data Models

### Message
```json
{
  "role": "string",
  "parts": [
    {
      "text": "string"
    }
  ]
}
```

### ChatRequest
```json
{
  "contents": [
    {
      "role": "string",
      "parts": [
        {
          "text": "string"
        }
      ]
    }
  ]
}
```

## Rate Limits
No rate limits currently implemented.

## CORS
CORS is enabled for all origins in development. Configure appropriately for production.

## Interactive Documentation
FastAPI provides interactive API documentation:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`