# Clau - Financial Advisory Chatbot Backend

A FastAPI-powered backend service that provides AI-driven financial advisory responses using Google Gemini 2.5 Flash API.

## 🚀 Features

- **FastAPI Framework**: High-performance, modern Python web framework
- **Google Gemini Integration**: Powered by Gemini 2.5 Flash for intelligent responses
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Professional Financial Advisor**: Specialized AI persona for financial guidance
- **RESTful API**: Clean, documented API endpoints
- **Environment Configuration**: Secure API key management

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **AI Model**: Google Gemini 2.5 Flash
- **HTTP Client**: Requests
- **Environment**: Python-dotenv
- **Data Validation**: Pydantic
- **Server**: Uvicorn

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Clau_AI_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Mac/Linux
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` file and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

6. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

7. **Access the API**
   - **Live API**: [https://clau-ai-backend.onrender.com](https://clau-ai-backend.onrender.com)
   - **Local Development**: `http://localhost:8000`
   - **API Documentation**: `http://localhost:8000/docs`

## 📡 API Endpoints

### GET `/`
Health check endpoint
```json
{
  "message": "Financial Advisory Chatbot Backend is running"
}
```

### POST `/ask`
Send financial questions and receive AI-powered advice

**Request Body:**
```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "How should I budget my monthly income?"
        }
      ]
    }
  ]
}
```

**Response:**
```json
{
  "answer": "AI-generated financial advice response"
}
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Dependencies
```
fastapi
uvicorn[standard]
python-dotenv
requests
pydantic
```

## 🏗️ Deployment

The backend is deployed on Render and automatically handles:
- Environment variable configuration
- CORS for frontend communication
- Production-ready server setup

## 📁 Project Structure

```
Clau_AI_backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── runtime.txt         # Python version specification
├── .env.example        # Environment template
├── .env               # Environment variables (not in repo)
└── .gitignore         # Git ignore rules
```

## 🎯 AI Persona

The backend implements "Clau" - a professional financial advisor with:
- Expert knowledge in personal finance
- Clear, concise communication style
- Personalized recommendations
- No disclaimers policy for streamlined advice
- Proactive guidance approach

## 📄 License

This project is licensed under the MIT License.