# Architecture Documentation

## System Overview
The Clau Financial Advisory Chatbot follows a client-server architecture with clear separation between frontend and backend services.

## Components

### Backend Service (FastAPI)
- **Framework**: FastAPI with Uvicorn server
- **AI Integration**: Google Gemini 2.5 Flash API
- **Data Validation**: Pydantic models
- **CORS**: Enabled for cross-origin requests

### Key Features
- RESTful API design
- Async request handling
- Environment-based configuration
- Error handling and validation

## Data Flow

```
User Input → Frontend → Backend API → Gemini API → Response → Frontend → User
```

1. User submits financial question via frontend
2. Frontend sends POST request to `/ask` endpoint
3. Backend processes request and adds system prompt
4. Backend calls Gemini API with conversation context
5. Gemini returns AI-generated financial advice
6. Backend returns formatted response to frontend
7. Frontend displays response to user

## System Prompt
The backend injects a comprehensive system prompt that defines:
- AI persona as "Clau" - professional financial advisor
- Response format and style guidelines
- Financial expertise areas
- User interaction patterns
- Output formatting requirements

## Request Processing
1. **Validation**: Pydantic models validate incoming requests
2. **Prompt Injection**: System prompt added to first user message
3. **API Call**: Request forwarded to Gemini API
4. **Response Processing**: Extract and format AI response
5. **Error Handling**: Graceful error responses for failures

## Security Considerations
- API keys stored in environment variables
- CORS configured for production
- Input validation via Pydantic models
- Error handling prevents information leakage

## Scalability
- Stateless design for horizontal scaling
- Async FastAPI for concurrent request handling
- Environment-based configuration for different deployments

## Deployment Architecture
- **Backend**: Deployed on Render
- **Environment**: Production-ready configuration
- **Monitoring**: Health check endpoint available
- **Documentation**: Auto-generated OpenAPI specs