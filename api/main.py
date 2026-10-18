import time
import uuid

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent.final_agent import FinalAgent
from agent.logger import AgentLogger


app = FastAPI(
    title="Naukri Support Agent API",
    description="AI-powered Naukri job application support agent",
    version="1.0.0"
)

agent = FinalAgent()
logger = AgentLogger()


class ChatRequest(BaseModel):
    message: str


# ---------------------------------------------------------
# HTTP REQUEST MIDDLEWARE
# ---------------------------------------------------------

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """
    Adds a unique trace ID and measures request duration.
    """

    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id

    start_time = time.perf_counter()

    response = await call_next(request)

    duration_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2
    )

    response.headers["X-Trace-ID"] = trace_id
    response.headers["X-Process-Time-ms"] = str(duration_ms)

    return response


# ---------------------------------------------------------
# API ROOT
# ---------------------------------------------------------

@app.get("/api")
def api_root():
    return {
        "status": "success",
        "message": "Naukri Support Agent API is running"
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "agent": "Naukri Support Agent"
    }


# ---------------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest, http_request: Request):

    start_time = time.perf_counter()

    result = agent.process(request.message)

    duration_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2
    )

    trace_id = http_request.state.trace_id

    # Determine logging fields from agent response
    response_type = result.get("type")
    source = result.get("source")
    status = result.get("status", "SUCCESS")

    if status == "BLOCKED":
        guardrail_status = "BLOCKED"
    else:
        guardrail_status = "ALLOWED"

    # Log the request
    logger.log_request(
        user_message=request.message,
        response_type=response_type,
        selected_tool=source,
        guardrail_status=guardrail_status,
        status=status,
        trace_id=trace_id,
        duration_ms=duration_ms,
        method="POST",
        path="/chat",
        status_code=200
    )

    return result


# ---------------------------------------------------------
# WEBSOCKET CHAT
# ---------------------------------------------------------

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):

    await websocket.accept()

    try:

        while True:

            message = await websocket.receive_text()

            start_time = time.perf_counter()

            result = agent.process(message)

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2
            )

            trace_id = str(uuid.uuid4())

            response_type = result.get("type")
            source = result.get("source")
            status = result.get("status", "SUCCESS")

            if status == "BLOCKED":
                guardrail_status = "BLOCKED"
            else:
                guardrail_status = "ALLOWED"

            logger.log_request(
                user_message=message,
                response_type=response_type,
                selected_tool=source,
                guardrail_status=guardrail_status,
                status=status,
                trace_id=trace_id,
                duration_ms=duration_ms,
                method="WEBSOCKET",
                path="/ws/chat",
                status_code=200
            )

            await websocket.send_json(result)

    except WebSocketDisconnect:

        print("WebSocket client disconnected")


# ---------------------------------------------------------
# FRONTEND
# ---------------------------------------------------------

app.mount(
    "/",
    StaticFiles(
        directory="frontend",
        html=True
    ),
    name="frontend"
)