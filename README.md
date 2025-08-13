# Clau - Financial Advisory Chatbot Backend

A FastAPI-powered backend service that provides AI-driven financial advisory responses using Google Gemini 2.5 Flash API.

## 🚀 Features

- **FastAPI Framework**: High-performance, modern Python web framework
- **Google Gemini Integration**: Powered by Gemini 2.5 Flash for intelligent responses
- **Rich Formatting**: Advanced markdown with tables, headers, and visual cards
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
- Node.js (for frontend) - [Download here](https://nodejs.org/en/download)
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
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── requirements-test.txt    # Testing dependencies
├── test_main.py            # Comprehensive test suite
├── runtime.txt             # Python version specification
├── API_DOCUMENTATION.md    # Detailed API reference
├── ARCHITECTURE.md         # System architecture guide
├── DEPLOYMENT.md           # Deployment instructions
├── PROMPT_ENGINEERING.md   # AI prompt optimization guide
├── .env.example            # Environment template
├── .env                   # Environment variables (not in repo)
└── .gitignore             # Git ignore rules
```

## 🎯 AI Persona

The backend implements "Clau" - a professional financial advisor with:
- Expert knowledge in personal finance
- Clear, concise communication style
- Rich markdown formatting with tables and visual cards
- Personalized recommendations
- Appropriate disclaimers for investment advice
- Proactive guidance approach

## 🧪 Testing

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest test_main.py -v

# Run specific test
pytest test_main.py::test_ask_success -v

# Run tests with coverage
pytest test_main.py --cov=main
```

### Test Coverage
- Health check endpoint validation
- Chat API request/response handling
- Error handling and edge cases
- Gemini API integration testing
- Input validation and sanitization

## 📋 Sample Financial Questions Test Suite

The chatbot handles these assessment questions effectively:

1. **"What is the difference between a Roth IRA and a Traditional IRA?"**
   - Expected: Tax treatment comparison, contribution limits, withdrawal rules

2. **"How should I allocate my 401(k) investments?"**
   - Expected: Age-based allocation, risk tolerance, diversification strategies

3. **"What's a good debt-to-income ratio?"**
   - Expected: Specific percentage ranges (28/36 rule), impact on financial health

4. **"How do I create an emergency fund?"**
   - Expected: Step-by-step process, 3-6 months expenses, high-yield savings

5. **"Should I pay off my student loans or invest in the stock market?"**
   - Expected: Interest rate comparison, risk analysis, balanced approach

6. **"What is dollar-cost averaging?"**
   - Expected: Definition, benefits, implementation strategy with examples

7. **"How do interest rate changes affect my mortgage?"**
   - Expected: Fixed vs variable rates, refinancing considerations

8. **"What's the rule of 72?"**
   - Expected: Formula explanation, doubling time calculations, practical examples

9. **"How much should I save for retirement?"**
   - Expected: 10-15% rule, employer matching, compound interest benefits

10. **"What are current market trends affecting tech stocks?"**
    - Expected: General market factors, sector analysis, investment considerations

**Testing Instructions:**
- Use the live demo or local setup to test these questions
- Verify responses include tables, headers, and **Final Recommendation** format
- Check for appropriate disclaimers on investment advice
- See `TEST_SUITE.md` for detailed test cases and expected responses

## 📚 Documentation

Comprehensive documentation is available in separate files:

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**: Complete API reference with examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System design and data flow
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Production deployment guide
- **[PROMPT_ENGINEERING.md](PROMPT_ENGINEERING.md)**: AI prompt optimization techniques

## 🛠️ Development Decisions & Challenges Overcome

### Architecture Choices
- **FastAPI Framework**: Selected for high performance, automatic API documentation, and modern Python async support
- **Pydantic Models**: Ensures type safety and automatic request validation for robust API design
- **Environment Configuration**: Secure API key management using python-dotenv for production safety
- **CORS Middleware**: Enables seamless frontend-backend communication across different domains

### Challenges Overcome
1. **Prompt Engineering Complexity**: Developed a comprehensive 23-instruction system prompt to ensure consistent, professional financial advice across all queries
2. **Response Formatting**: Implemented rich markdown formatting with tables, headers, and visual cards for enhanced readability
3. **Error Handling**: Created robust error handling for API failures, timeouts, and invalid responses with user-friendly messages
4. **API Integration**: Successfully integrated with Gemini 2.5 Flash API using proper authentication and request formatting
5. **Production Deployment**: Configured secure environment variables and CORS policies for live deployment

## 🔮 Future Improvements

### Planned Features
1. **User Authentication**: Implement user accounts for personalized financial tracking and conversation history
2. **Financial Calculators**: Add built-in calculators for loans, investments, retirement planning, and mortgage calculations
3. **Document Analysis**: Enable users to upload financial documents (bank statements, tax forms) for AI analysis
4. **Multi-language Support**: Expand to support Spanish, French, and other languages for broader accessibility
5. **Voice Interface**: Integrate speech-to-text and text-to-speech for hands-free financial consultations

### Technical Enhancements
1. **Caching Layer**: Implement Redis caching for common financial queries to improve response times
2. **Rate Limiting**: Add API rate limiting and usage analytics for production scalability
3. **Database Integration**: Add PostgreSQL for user data, conversation history, and financial goal tracking
4. **Advanced Analytics**: Implement user behavior analytics and A/B testing for prompt optimization
5. **Microservices Architecture**: Split into specialized services for different financial domains (investments, loans, budgeting)

## 🤖 Prompt Engineering Documentation

Detailed prompt engineering techniques used with Gemini API are documented in `PROMPT_ENGINEERING.md`, including:

- **System Prompt Architecture**: 23-instruction framework for consistent financial advice
- **Advanced Techniques**: Negative prompting, few-shot learning, chain-of-thought prompting
- **Response Quality Optimization**: Behavioral conditioning and format specifications
- **Visual Structure**: Markdown formatting with tables, headers, and cards
- **Constraint-Based Prompting**: Role definition, domain boundaries, and behavioral rules
- **Multi-Modal Instruction Layering**: Identity, capability, behavioral, and format instructions

## 📄 License

This project is licensed under the MIT License.

## 🚀 Live Demo

**API Endpoint**: [https://clau-ai-backend.onrender.com](https://clau-ai-backend.onrender.com)
**Interactive Docs**: [https://clau-ai-backend.onrender.com/docs](https://clau-ai-backend.onrender.com/docs)
**Frontend**: [https://financialadvisorychatbot.vercel.app/](https://financialadvisorychatbot.vercel.app/)