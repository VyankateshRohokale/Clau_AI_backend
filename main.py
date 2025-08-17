# Last change by Vyankatesh Rohokale on 12/08/2025 (dd/mm/yyyy)

"""
Clau - Financial Advisory Chatbot Backend

FastAPI backend that proxies Google Gemini 2.5 Flash with:
- Financial domain system prompt
- Robust retries and error handling
- Output post-processing (table fix, strip bold in cells, line wrapping, disclaimer)
- Lightweight category tagging + rich metadata for dashboard insights
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import os
import time
import re
import requests
from dotenv import load_dotenv

# -----------------------------
# Environment / App bootstrap
# -----------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

app = FastAPI(
    title="Clau Financial Advisory API",
    description="AI-powered financial advisory chatbot backend",
    version="1.2.0",
)

# CORS – tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # TODO: Restrict to your domains in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Pydantic models
# -----------------------------
class Message(BaseModel):
    role: str                   # 'user' | 'model'
    parts: List[Dict[str, Any]] # e.g., [{"text": "Hello"}]

class ChatRequest(BaseModel):
    contents: List[Message]

class ChatResponse(BaseModel):
    answer: str
    meta: Dict[str, Any]        # category, has_disclaimer, retries, model, response_length, timestamp

# -----------------------------
# System Prompt (financial)
# -----------------------------
SYSTEM_PROMPT = """
You are a professional, helpful, and highly knowledgeable financial advisor chatbot named "Clau".
Your primary goal is to provide accurate, clear, and concise financial guidance.

Mandatory Table Formatting Rule:
Every table MUST follow this exact Markdown structure:
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1    | Row 1    | Row 1    |
| Row 2    | Row 2    | Row 2    |

- The header separator line (---------) is REQUIRED for every table, also use vertical lines
- Never bold table cell content; use bold only outside tables.
- Keep table text concise for mobile readability.
- Use tables wherever they clarify comparisons.
- Use Dates, Values, Percentages, and Timeframes as much possible.

Responsibilities:
1) Advise on personal finance, saving, debt, investments, retirement, college planning, and financial literacy.
2) Explain complex topics simply; use bullets, tables, headers, and blockquotes.
3) When answering about market trends or economic indicators, always include:
   - The **most recent date** of the data
   - **Exact numerical values** (percentages, dollar amounts, index points)
   - **Relevant timeframes** (e.g., “past 6 months”, “since Jan 2024”)
   - **Source name** (e.g., “Source: Bloomberg”)
4) When giving investment-related advice, include this disclaimer at the end:
5) Keep responses concise but complete; avoid greetings.
6) Format numbers clearly: percentages, $ amounts, and timeframes.
7) Ask for missing key inputs only when needed; do NOT repeat asks already provided.
8) End with a bold Final Recommendation line, e.g., **Final Recommendation: Save $200 and cap wants at $300.**
"""

DISCLAIMER_TEXT = (
    "Disclaimer: This is for informational purposes only and not professional financial advice. "
    "Consult a certified financial planner or tax professional for personalized guidance."
)

# -----------------------------
# Helpers: category, disclaimer
# -----------------------------
INVESTMENT_KEYWORDS = [
    "stock", "stocks", "bond", "bonds", "mutual fund", "etf", "portfolio",
    "asset allocation", "diversification", "brokerage", "retirement", "401(k)",
    "roth", "ira", "market", "equity", "securities", "dividend"
]

CATEGORY_MAP = {
    "personal_finance": [
        "budget", "budgeting", "save", "saving", "debt", "loan", "rent", "groceries",
        "emergency fund", "expense", "utilities", "credit score", "dti", "spend"
    ],
    "investments": INVESTMENT_KEYWORDS,
    "financial_planning": [
        "retirement", "401(k)", "roth", "ira", "college", "529", "pension",
        "estate", "insurance", "planning", "goal"
    ],
    "financial_literacy": [
        "compound interest", "apr", "apy", "rule of 72", "inflation", "amortization",
        "interest rate", "depreciation"
    ],
    "market_trends": [
        "cpi", "inflation", "interest rates", "fed", "gdp", "unemployment",
        "oil prices", "market trend", "economic indicator", "yield curve", "central bank"
    ],
}

def detect_category(text: str) -> str:
    t = text.lower()
    for cat, keys in CATEGORY_MAP.items():
        if any(k in t for k in keys):
            return cat
    if any(k in t for k in INVESTMENT_KEYWORDS):
        return "investments"
    return "personal_finance"

def is_investment_related(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in INVESTMENT_KEYWORDS)

def ensure_disclaimer(answer: str) -> Tuple[str, bool]:
    """
    Append disclaimer if content appears investment-related and disclaimer not already present.
    """
    has = ("informational purposes only" in answer.lower()
           and "not professional financial advice" in answer.lower())
    if is_investment_related(answer) and not has:
        if not answer.endswith("\n"):
            answer += "\n"
        answer += f"\n{DISCLAIMER_TEXT}"
        return answer, True
    return answer, has

# -----------------------------
# Post-processing: tables & formatting
# -----------------------------
TABLE_HEADER_RE = re.compile(r'^\|(.+?)\|\s*$', re.MULTILINE)

def _looks_like_separator(line: str) -> bool:
    return bool(re.match(r'^\|\s*:?-{3,}\s*(\|\s*:?-{3,}\s*)+\|?\s*$', line.strip()))

def fix_markdown_tables(text: str) -> str:
    """
    Ensure any markdown table header line is followed by a separator line like:
    |-----|-----|-----|
    Only inserts if the immediate next non-empty line is not already a valid separator.
    """
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if '|' in line.strip() and TABLE_HEADER_RE.match(line.strip()):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                out.append(lines[j])
                j += 1
            if j < len(lines):
                next_line = lines[j]
                if not _looks_like_separator(next_line):
                    cols = [c.strip() for c in line.strip().split('|') if c.strip() != '']
                    if cols:
                        sep = "|" + "|".join(["----------"] * len(cols)) + "|"
                        out.append(sep)
            else:
                cols = [c.strip() for c in line.strip().split('|') if c.strip() != '']
                if cols:
                    sep = "|" + "|".join(["----------"] * len(cols)) + "|"
                    out.append(sep)
        i += 1
    return "\n".join(out)

BOLD_IN_CELL_RE = re.compile(r'(\|[^|\n]*?)\*\*(.+?)\*\*([^|\n]*?\|)')

def strip_bold_inside_table_cells(text: str) -> str:
    """
    Remove **bold** inside table rows (leaves normal text), preserving outside-table bold.
    """
    def _replace_line(line: str) -> str:
        # Don't modify header-separator lines
        if _looks_like_separator(line):
            return line
        # Replace all bold segments inside cell content for the line
        new_line = line
        while True:
            m = BOLD_IN_CELL_RE.search(new_line)
            if not m:
                break
            new_line = new_line[:m.start()] + m.group(1) + m.group(2) + m.group(3) + new_line[m.end():]
        return new_line

    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith("|"):
            lines[idx] = _replace_line(line)
    return "\n".join(lines)

def soft_wrap_lines(text: str, max_len: int = 109) -> str:
    """
    Soft-wrap lines to <= max_len chars, skipping:
    - table lines (start with '|')
    - table separator lines
    - code fences and content within ``` blocks
    - URLs (lines containing 'http'/'https')
    - blockquote lines (start with '>')
    """
    out = []
    in_code = False
    for line in text.splitlines():
        striped = line.strip()
        if striped.startswith("```"):
            out.append(line)
            in_code = not in_code
            continue
        if in_code or striped.startswith("|") or _looks_like_separator(line) or striped.startswith(">"):
            out.append(line)
            continue
        if "http://" in line or "https://" in line:
            out.append(line)
            continue

        if len(line) <= max_len:
            out.append(line)
            continue

        # wrap by words
        words = line.split(" ")
        cur = ""
        for w in words:
            if len(cur) + (1 if cur else 0) + len(w) <= max_len:
                cur = w if not cur else f"{cur} {w}"
            else:
                out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return "\n".join(out)

# -----------------------------
# Gemini call with retries
# -----------------------------
def call_gemini(payload: Dict[str, Any], max_retries: int = 3, base_delay: float = 0.8) -> Dict[str, Any]:
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")

    headers = {"Content-Type": "application/json"}
    last_err_text = ""
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(
                f"{GEMINI_URL}?key={GEMINI_API_KEY}",
                json=payload,
                headers=headers,
                timeout=30,
            )
            if resp.status_code == 200:
                return {"json": resp.json(), "retries": attempt - 1}
            if resp.status_code in (429, 500, 502, 503, 504):
                last_err_text = resp.text
                time.sleep(base_delay * (2 ** (attempt - 1)))
                continue
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        except requests.exceptions.Timeout:
            if attempt == max_retries:
                raise HTTPException(status_code=504, detail="Request to AI service timed out")
            time.sleep(base_delay * (2 ** (attempt - 1)))
        except requests.exceptions.RequestException:
            if attempt == max_retries:
                raise HTTPException(status_code=502, detail="AI service temporarily unavailable")
            time.sleep(base_delay * (2 ** (attempt - 1)))
    raise HTTPException(status_code=502, detail=last_err_text or "AI service temporarily unavailable")

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def health_check():
    return {"message": "Financial Advisory Chatbot Backend is running"}

@app.post("/ask", response_model=ChatResponse)
def ask_question(data: ChatRequest):
    """
    Process financial advisory questions using Google Gemini API with:
    - system prompt injection   
    - retries
    - table/disclaimer/bold-in-cell/line-wrap post-processing
    - category tagging and rich metadata
    """
    if not data.contents:
        raise HTTPException(status_code=400, detail="contents cannot be empty")

    # Inject system prompt by prepending it to the first user message
    first_user = next((m for m in data.contents if m.role.lower() == "user"), None)
    if first_user and first_user.parts and isinstance(first_user.parts[0], dict):
        original = first_user.parts[0].get("text", "")
        first_user.parts[0]["text"] = f"{SYSTEM_PROMPT}\n\nUser question:\n{original}"

    payload = {"contents": [m.model_dump() for m in data.contents]}

    result = call_gemini(payload)
    retries_used = result["retries"]
    raw = result["json"]

    # Parse Gemini response
    try:
        text = raw.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except Exception:
        raise HTTPException(status_code=502, detail="Invalid response from AI service")

    if not text:
        raise HTTPException(status_code=502, detail="AI service returned empty response")

    # Post-processing pipeline
    text = fix_markdown_tables(text)
    text = strip_bold_inside_table_cells(text)
    text = soft_wrap_lines(text, max_len=109)
    text, has_disclaimer = ensure_disclaimer(text)

    # Category tagging for dashboard (prefer user message for intent)
    user_text = ""
    if first_user and first_user.parts and isinstance(first_user.parts[0], dict):
        user_text = first_user.parts[0].get("text", "")
    category = detect_category(user_text or text)

    # Meta for dashboard/insights
    meta = {
        "category": category,
        "has_disclaimer": has_disclaimer,
        "retries": retries_used,
        "model": GEMINI_MODEL,
        "response_length": len(text),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    return ChatResponse(answer=text, meta=meta)
