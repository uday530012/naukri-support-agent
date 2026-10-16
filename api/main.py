from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent.final_agent import FinalAgent


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Naukri Support Agent API",
    description="AI-powered Naukri job application support agent",
    version="1.0.0"
)


# ============================================================
# INITIALIZE AGENT
# ============================================================

agent = FinalAgent()


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    message: str


# ============================================================
# ROOT API
# ============================================================

@app.get("/api")
def api_root():

    return {
        "status": "success",
        "message": "Naukri Support Agent API is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "agent": "Naukri Support Agent"
    }


# ============================================================
# CHAT ENDPOINT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    result = agent.process(request.message)

    return result


# ============================================================
# FRONTEND
# ============================================================

app.mount(
    "/",
    StaticFiles(
        directory="frontend",
        html=True
    ),
    name="frontend"
)