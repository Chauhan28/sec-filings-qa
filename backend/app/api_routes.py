# # backend/app/api_routes.py

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from .rag_pipeline import ask_question

# router = APIRouter()

# # Define input format
# class QuestionRequest(BaseModel):
#     question: str

# # Define output format
# class AnswerResponse(BaseModel):
#     answer: str
#     sources: list[str]

# @router.post("/ask", response_model=AnswerResponse)
# def ask(request: QuestionRequest):
#     try:
#         answer, sources = ask_question(request.question)
#         source_names = [doc.metadata.get("ticker", "Unknown") for doc in sources]
#         return {"answer": answer, "sources": list(set(source_names))}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


import time
from collections import defaultdict, deque

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .rag_pipeline import ask_question

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

# --- simple per-IP rate limit (protects your Groq free-tier quota) ---
RATE_LIMIT = 10          # questions allowed...
WINDOW_SECONDS = 60      # ...per this many seconds, per visitor
MAX_QUESTION_CHARS = 500
_hits = defaultdict(deque)

def _client_ip(req: Request) -> str:
    fwd = req.headers.get("x-forwarded-for")
    return fwd.split(",")[0].strip() if fwd else (req.client.host if req.client else "unknown")

def _error(status: int, message: str):
    # Includes an "answer" key so the chat page shows the message instead of crashing
    return JSONResponse(
        status_code=status,
        content={"answer": message, "sources": [], "detail": message},
    )

@router.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest, http_request: Request):
    question = request.question.strip()
    if not question:
        return _error(400, "Please type a question.")
    if len(question) > MAX_QUESTION_CHARS:
        return _error(400, f"Please keep questions under {MAX_QUESTION_CHARS} characters.")

    ip = _client_ip(http_request)
    now = time.time()
    q = _hits[ip]
    while q and now - q[0] > WINDOW_SECONDS:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return _error(429, "Too many questions too quickly. Please wait a minute and try again.")
    q.append(now)

    try:
        answer, sources = ask_question(question)
        source_names = sorted({doc.metadata.get("ticker", "Unknown") for doc in sources})
        return {"answer": answer, "sources": source_names}
    except Exception as e:
        print(f"/ask failed: {e!r}")  # full error stays in your terminal
        return _error(500, "Sorry, the AI service had a problem. Please try again in a moment.")