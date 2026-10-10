from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from .api_routes import router
from pathlib import Path
import random
import os

# === AUTH CODE
# Fixed code from .env; falls back to a random one if ACCESS_CODE is not set
AUTH_CODE = os.getenv("ACCESS_CODE") or str(random.randint(100000, 999999))
SHOW_CODE = os.getenv("SHOW_CODE", "false").lower() == "true"

# === RICH TERMINAL OUTPUT ===
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

console = Console()

# Environment setup info
console.rule("[bold red]🚨 IMPORTANT SETUP REQUIRED")
console.print(Text("Set GROQ_API_KEY (and optionally ACCESS_CODE) in the .env file at the repo root.\n", style="bold yellow"))

# Project Info
title_panel = Panel.fit(
    Text("🤖 genai-sec10k-insights", justify="left"),
    title="AI-Powered SEC 10-K Chatbot",
    border_style="cyan"
)
console.print(title_panel)

project_description = """
An AI-powered web app to chat with SEC 10-K filings using OpenAI, LangChain, and FAISS.

🔍 Ask about:
• Revenue, income, and expenses for companies like Apple, Tesla, Microsoft, etc.
• Risk disclosures, litigation issues, R&D, regional revenue, and more.

📦 Tech Stack:
• Backend: FastAPI, LangChain, OpenAI
• Frontend: Custom HTML/CSS/JS
• Vector DB: FAISS
• Containerized: Docker-ready
"""
console.print(Markdown(project_description))

auth_panel = Panel.fit(
    Text(f"{AUTH_CODE}", justify="center", style="bold white on green"),
    title="🔐 AUTH CODE - ENTER THIS TO ACCESS APP",
    border_style="magenta",
    padding=(1, 10)
)
console.print(auth_panel)

instructions = """
📌 Usage Instructions:
- Visit http://localhost:8000 in your browser
- Enter the 6-digit code shown above
- After authentication, you'll be redirected to the chat UI
- To test backend APIs, use Swagger UI at /docs
"""
console.print(Markdown(instructions))
console.rule("[bold white]🚀 Launching FastAPI server...")

# === APP SETUP
app = FastAPI(
    title="genai-sec10k-insights",
    description="Ask questions over SEC 10-K filings using RAG",
    version="1.0.0",
    docs_url=None,  # disable default docs
    redoc_url=None,
    openapi_url=None,
)

# === CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === STATIC PATHS
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# === AUTH MIDDLEWARE
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # Allow /, /validate-code, /static, and favicon.ico through
        if path.startswith("/static") or path in ["/", "/validate-code", "/favicon.ico"]:
            return await call_next(request)
        # Check auth cookie
        if request.cookies.get("auth_passed") != "true":
            return RedirectResponse(url="/")
        return await call_next(request)

app.add_middleware(AuthMiddleware)

# === ROUTES
@app.get("/", response_class=HTMLResponse)
async def get_auth_page():
    auth_path = FRONTEND_DIR / "auth.html"
    with open(auth_path, "r") as f:
        html = f.read()
    if SHOW_CODE:
        hint = (
            '<p style="position:fixed;bottom:16px;left:0;right:0;text-align:center;'
            'color:#fff;font-family:sans-serif;">Demo access code: '
            f'<b>{AUTH_CODE}</b></p>'
        )
        html = html.replace("</body>", hint + "</body>") if "</body>" in html else html + hint
    return HTMLResponse(content=html)

@app.post("/validate-code")
async def validate_code(data: dict):
    if str(data.get("code", "")).strip() == AUTH_CODE:
        response = RedirectResponse(url="/chat", status_code=302)
        response.set_cookie("auth_passed", "true", httponly=True, samesite="lax")
        return response
    return JSONResponse({"error": "Invalid code"}, status_code=401)

@app.get("/chat", response_class=HTMLResponse)
async def serve_chat():
    index_path = FRONTEND_DIR / "index.html"
    with open(index_path, "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/docs", response_class=HTMLResponse)
async def get_custom_docs():
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url="/openapi.json", title="genai-sec10k-insights Docs")

@app.get("/openapi.json", include_in_schema=False)
async def openapi_json():
    return app.openapi()

# === API ROUTES
app.include_router(router)
