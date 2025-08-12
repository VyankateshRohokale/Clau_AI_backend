# Deployment Guide

## Prerequisites
- Python 3.8+
- Google Gemini API key
- Render account (for production)

## Local Development

1. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

4. **Run Development Server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Verify Installation**
   - Visit `http://localhost:8000` for health check
   - Visit `http://localhost:8000/docs` for API documentation

## Production Deployment (Render)

### Step 1: Repository Setup
1. Push code to GitHub repository
2. Ensure all files are committed:
   - `main.py`
   - `requirements.txt`
   - `runtime.txt`
   - `.env.example`

### Step 2: Render Configuration
1. **Connect Repository**
   - Link GitHub repository to Render
   - Select Python environment

2. **Configure Build Settings**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Python Version**: Specified in `runtime.txt`

3. **Environment Variables**
   - Set `GEMINI_API_KEY` in Render dashboard
   - `PORT` is automatically set by Render

### Step 3: Deploy
1. Trigger deployment from Render dashboard
2. Monitor build logs for any issues
3. Verify deployment via health check endpoint

## Environment Variables

### Required
- `GEMINI_API_KEY`: Your Google Gemini API key

### Optional
- `PORT`: Server port (default: 8000, auto-set by Render)

## Monitoring and Maintenance

### Health Checks
- **Endpoint**: `GET /`
- **Expected Response**: `{"message": "Financial Advisory Chatbot Backend is running"}`

### Logs
- Available in Render dashboard
- Monitor for API errors and performance issues

### API Documentation
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Troubleshooting

### Common Issues
1. **API Key Missing**: Ensure `GEMINI_API_KEY` is set in environment
2. **CORS Errors**: Verify CORS middleware configuration
3. **Build Failures**: Check `requirements.txt` and Python version

### Debug Steps
1. Check Render build logs
2. Verify environment variables
3. Test API endpoints manually
4. Review application logs for errors

## Performance Optimization
- Use production ASGI server (Uvicorn)
- Configure appropriate worker processes
- Monitor response times and error rates
- Implement caching if needed

## Security Best Practices
- Keep API keys secure in environment variables
- Configure CORS for specific origins in production
- Regularly update dependencies
- Monitor for security vulnerabilities