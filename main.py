# Last change by Vyankatesh Rohokale on 12/08/2025 (dd/mm/yyyy)


#Imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# Allow all origins for local development (CORS fix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# sending a request to Gemini API
class Message(BaseModel):
    role: str
    parts: List[dict]


# Request model for the chat
class ChatRequest(BaseModel):
    contents: List[Message]

# class QuestionRequest(BaseModel):
#     question: str

@app.get("/")
def root():
    return {"message": "Financial Advisory Chatbot Backend is running"}

@app.post("/ask")
def ask_question(data: ChatRequest):
    if not GEMINI_API_KEY: # check for API key
        raise HTTPException(status_code=500, detail="Gemini API Key not set")

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
    User question:   

       13.  *Always be helpful and polite.*
       14. **if user is rude , still reply calmly and politely**
       15.  *Provide accurate, factual information.* Do not hallucinate data.
       16.  *Explain complex concepts simply.* Use analogies and bullet points to make information easy to understand.
       17.  *Format responses clearly.* Use bolding for key terms, percentages, and dollar amounts.
       18.  *Include a disclaimer for investment advice.* For any investment-related question, end the response with: "Disclaimer: This is for informational purposes only and not professional financial advice. Consult a certified financial planner or tax professional for personalized guidance."
       19.  *Handle non-financial queries gracefully.* Politely state that you are a financial assistant and can only answer questions related to finance.
       20.  *Respond to numerical questions with relevant data.* For example, when asked about a debt-to-income ratio, provide the generally accepted "good" range.
       21. **Disclaimers**: Include disclaimers for investment advice as appropriate 
  """

    
    
    # To add system prompt to the first user message
    if data.contents:
        first_user_message = next((msg for msg in data.contents if msg.role == 'user'), None)
        if first_user_message:
            if first_user_message.parts and first_user_message.parts[0].get('text'):
                first_user_message.parts[0]['text'] = system_prompt + "\n" + first_user_message.parts[0]['text']

    
    # Call for Gemini API
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    


    payload = {
        "contents": [msg.model_dump() for msg in data.contents]
    }


    try:
        response = requests.post(f"{url}?key={GEMINI_API_KEY}", json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    result = response.json()
    answer = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    return {"answer": answer}





