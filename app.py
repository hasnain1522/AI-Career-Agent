from pathlib import Path
import threading
import time
import uuid

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents import Runner

from main import agent, UserContext, get_user_session


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "Frontend"


app = FastAPI(
    title="CareerGuide AI",
    description="AI-powered career, job and business guidance agent.",
    version="1.0.0",
)


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

app.mount(
    "/frontend",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="frontend",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request model
# ---------------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    user_id: str | None = Field(default=None, max_length=100)


# ---------------------------------------------------------
# Basic application-level rate limiting
# ---------------------------------------------------------

RATE_LIMIT_WINDOW = 60
MAX_REQUESTS_PER_USER = 5
MAX_REQUESTS_GLOBAL = 8

_rate_limit_lock = threading.Lock()
_user_request_times: dict[str, list[float]] = {}
_global_request_times: list[float] = []


def check_rate_limit(user_id: str) -> bool:
    """
    Returns True when the request should be blocked.

    This protects the public application from accidentally
    generating too many OpenAI requests in a short period.
    """

    now = time.monotonic()
    cutoff = now - RATE_LIMIT_WINDOW

    with _rate_limit_lock:
        global _global_request_times

        # Remove expired global requests.
        _global_request_times = [
            timestamp
            for timestamp in _global_request_times
            if timestamp > cutoff
        ]

        # Remove expired requests for this user.
        user_times = _user_request_times.get(user_id, [])
        user_times = [
            timestamp
            for timestamp in user_times
            if timestamp > cutoff
        ]

        if len(_global_request_times) >= MAX_REQUESTS_GLOBAL:
            _user_request_times[user_id] = user_times
            return True

        if len(user_times) >= MAX_REQUESTS_PER_USER:
            _user_request_times[user_id] = user_times
            return True

        # Accept this request.
        _global_request_times.append(now)
        user_times.append(now)
        _user_request_times[user_id] = user_times

        return False


# ---------------------------------------------------------
# Validation error handling
# ---------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "response": (
                "Please enter a message between 1 and 4,000 characters."
            )
        },
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "CareerGuide AI",
    }


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


# ---------------------------------------------------------
# Chat endpoint
# ---------------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:
        return {
            "response": "Please enter a message."
        }

    # Generate a server-side user ID when the client does not
    # provide one.
    user_id = (
        request.user_id.strip()
        if request.user_id and request.user_id.strip()
        else str(uuid.uuid4())
    )

    # Protect the OpenAI API from excessive requests.
    if check_rate_limit(user_id):
        return JSONResponse(
            status_code=429,
            content={
                "response": (
                    "You're sending messages a little too quickly. "
                    "Please wait a few seconds and try again."
                ),
                "user_id": user_id,
            },
        )

    try:
        context = UserContext(
            user_id=user_id
        )

        session = get_user_session(
            user_id
        )

        result = Runner.run_sync(
            agent,
            message,
            context=context,
            session=session,
        )

        return {
            "response": result.final_output,
            "user_id": user_id,
        }

    except Exception as error:

        print("ERROR:", repr(error))

        error_text = str(error).lower()
        error_type = error.__class__.__name__.lower()

        # OpenAI rate-limit / temporary capacity errors.
        if (
            "ratelimit" in error_type
            or "rate limit" in error_text
            or "429" in error_text
        ):
            return JSONResponse(
                status_code=429,
                content={
                    "response": (
                        "CareerGuide AI is temporarily busy. "
                        "Please try again in a little while."
                    ),
                    "user_id": user_id,
                },
            )

        # Billing / quota exhaustion.
        if (
            "insufficient_quota" in error_text
            or "credit balance" in error_text
            or "quota" in error_text
        ):
            return JSONResponse(
                status_code=503,
                content={
                    "response": (
                        "CareerGuide AI is temporarily unavailable. "
                        "Please try again later."
                    ),
                    "user_id": user_id,
                },
            )

        # Generic production-safe error.
        return JSONResponse(
            status_code=500,
            content={
                "response": (
                    "Sorry, I couldn't process your request right now. "
                    "Please try again."
                ),
                "user_id": user_id,
            },
        )