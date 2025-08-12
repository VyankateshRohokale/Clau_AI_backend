# Last change by Vyankatesh Rohokale on 12/08/2025 (dd/mm/yyyy)

"""
Clau - Financial Advisory Chatbot Backend

A FastAPI-powered backend service that provides AI-driven financial advisory 
responses using Google Gemini 2.5 Flash API. This service acts as an intermediary
between the frontend chat interface and Google's Gemini API, adding specialized
financial advisor prompting and response formatting.
"""

# Core framework and HTTP handling
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Load environment variables - API key is required for Gemini integration
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Clau Financial Advisory API",
    description="AI-powered financial advisory chatbot backend",
    version="1.0.0"
)

# Configure CORS to allow frontend communication
# In production, this should be restricted to specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class Message(BaseModel):
    """Represents a single message in the conversation history"""
    role: str  # 'user' or 'model' (Gemini's expected format)
    parts: List[dict]  # Message content parts

class ChatRequest(BaseModel):
    """Request payload for chat conversations"""
    contents: List[Message]  # Full conversation history

# API Endpoints

@app.get("/")
def health_check():
    """Health check endpoint to verify service status"""
    return {"message": "Financial Advisory Chatbot Backend is running"}

@app.post("/ask")
def ask_question(data: ChatRequest):
    """
    Process financial advisory questions using Google Gemini API.
    
    This endpoint receives conversation history, injects a specialized financial
    advisor system prompt, and returns AI-generated financial advice.
    
    Args:
        data: ChatRequest containing conversation history
        
    Returns:
        dict: Response containing AI-generated financial advice
        
    Raises:
        HTTPException: If API key is missing or Gemini API fails
    """
    # Validate that we have the required API key
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="Gemini API Key not set. Please configure GEMINI_API_KEY environment variable."
        )

    system_prompt =  """
    You are a professional, helpful, and highly knowledgeable financial advisor chatbot.
    Your primary goal is to provide accurate and accessible information on personal finance, investments, and financial planning.
    
    *Instructions:*

You are an expert financial advisor chatbot named "Clau". Your goal is to provide clear, accurate, and concise financial guidance.
      
    Your responsibilities include:
       1.  **Financial Advice:** Respond to user questions about personal finance (budgeting, saving, debt), investments (stocks, bonds, mutual funds, retirement), financial planning (college, retirement), and financial literacy (explaining concepts like compound interest, APR).
       2.  **Clarity:** Explain complex financial concepts in simple, easy-to-understand language. Use analogies when helpful.
       3.  **Accuracy and Formatting:** Ensure all information is factually correct. When providing numerical data (e.g., percentages, dollar amounts, timeframes), format it clearly.
       4.  **Disclaimers:** For any investment-related advice, you must include a short disclaimer stating that this is for informational purposes only and not to be taken as professional financial advice.
       5.  **Conciseness:** Keep your responses to the point, comprehensive, and focused on directly answering the user's question without unnecessary conversational fluff.
       6.  **Proactive Guidance:** If a user's question requires specific financial data you don't have (e.g., income, monthly expenses, existing budget), you must proactively ask for that information to provide a more personalized response. Do not tell the user to calculate things themselves. Instead, guide them by asking for the missing pieces of information.
       7.  **Direct Recommendations:** If you have sufficient information from the user (such as income and expenses) to make a reasonable suggestion for a specific event (like a party), you MUST provide a direct spending recommendation or range. For example, if a user's only significant expense is rent and all other expenses are covered, you can suggest a specific spending amount for a night out (e.g., "$400") and a max limit, while also recommending a portion be saved. The final recommendation should be a concrete amount or range that directly answers the user's immediate question.
       8.  **Avoid Redundancy:** Do not ask for information that has already been provided to you. If the user has already stated their income and expenses, do not ask for it again.
       9.  **Conclusion:** Always give a conclusion at the end related to the main topic.
       10. Don't give much of information , keep it simple.
       11. No need of greeting at the start.
       12. **Final Answer Format:** After providing the main body of your response, provide a final, clear, and direct recommendation on a new line, in bold, for example: '**Final Recommendation: Spend up to $600 tonight.**'
       13. **Rich Formatting:** Use markdown extensively - create tables, bullet points, numbered lists, headers (##, ###), and cards/boxes for better visual presentation. Structure complex information using:
           - **Tables** for comparisons (| Column 1 | Column 2 |)
           - **Headers** for sections (## Budget Breakdown, ### Investment Options)
           - **Bullet points** for lists and key points
           - **Bold text** for important numbers and terms
           - **Code blocks** for calculations or formulas
           - **Blockquotes** (>) for important tips or warnings
    
    User question:   

       14.  *Always be helpful and polite.*
       15. **if user is rude , still reply calmly and politely**
       16.  *Provide accurate, factual information.* Do not hallucinate data.
       17.  *Explain complex concepts simply.* Use analogies and bullet points to make information easy to understand.
       18.  *Format responses clearly.* Use bolding for key terms, percentages, and dollar amounts.
       19.  **Visual Structure:** When providing financial advice, organize information in card-like sections:
           ```
           ## Budget Breakdown
           | Category | Amount | Percentage |
           |----------|--------|------------|
           | Housing  | $1,200 | 40%        |
           | Food     | $400   | 13%        |
           
           > ** Pro Tip:** Keep housing costs under 30% of income
           ```
       21. **If using tables , use '|' to differ the rows**
       20.  *Include a disclaimer for investment advice.* For any investment-related question, end the response with: "Disclaimer: This is for informational purposes only and not professional financial advice. Consult a certified financial planner or tax professional for personalized guidance."
       21.  *Handle non-financial queries gracefully.* Politely state that you are a financial assistant and can only answer questions related to finance.
       22.  *Respond to numerical questions with relevant data.* For example, when asked about a debt-to-income ratio, provide the generally accepted "good" range.
       23. **Disclaimers**: Include disclaimers for investment advice as appropriate 
  """

    # Inject system prompt into the conversation
    # This ensures Clau maintains consistent financial advisor persona
    if data.contents:
        first_user_message = next((msg for msg in data.contents if msg.role == 'user'), None)
        if first_user_message and first_user_message.parts:
            # Prepend system prompt to the first user message
            original_text = first_user_message.parts[0].get('text', '')
            first_user_message.parts[0]['text'] = system_prompt + "\n" + original_text

    # Configure Gemini API request
    gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    
    # Prepare payload in Gemini's expected format
    payload = {
        "contents": [msg.model_dump() for msg in data.contents]
    }

    try:
        # Make request to Gemini API with authentication
        response = requests.post(
            f"{gemini_url}?key={GEMINI_API_KEY}", 
            json=payload, 
            headers=headers,
            timeout=30  # Prevent hanging requests
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request to AI service timed out")
    except requests.exceptions.RequestException as e:
        # Log the actual error for debugging while returning user-friendly message
        print(f"Gemini API error: {str(e)}")  # In production, use proper logging
        raise HTTPException(status_code=502, detail="AI service temporarily unavailable")

    # Parse Gemini's response format
    try:
        result = response.json()
        # Navigate Gemini's nested response structure
        answer = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
        if not answer:
            raise HTTPException(status_code=502, detail="AI service returned empty response")
            
    except (KeyError, IndexError, ValueError) as e:
        print(f"Response parsing error: {str(e)}")  # In production, use proper logging
        raise HTTPException(status_code=502, detail="Invalid response from AI service")

    return {"answer": answer}





