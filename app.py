from pathlib import Path
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents import Runner

from main import agent, UserContext, get_user_session


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "Frontend"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="CareerGuide AI",
    description="AI-powered career, job and business guidance agent.",
    version="1.0.0",
)


# ============================================================
# FRONTEND
# ============================================================

app.mount(
    "/frontend",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="frontend",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "CareerGuide AI",
    }


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/")
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


# ============================================================
# CHAT ENDPOINT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    # --------------------------------------------------------
    # Validate message
    # --------------------------------------------------------

    if not request.message.strip():
        return {
            "response": "Please enter a message."
        }

    try:

        # ----------------------------------------------------
        # Create anonymous user ID if necessary
        # ----------------------------------------------------

        user_id = request.user_id

        if not user_id:
            user_id = str(uuid.uuid4())


        # ----------------------------------------------------
        # Create user-specific context
        # ----------------------------------------------------

        context = UserContext(
            user_id=user_id
        )


        # ----------------------------------------------------
        # Create user-specific conversation session
        # ----------------------------------------------------

        session = get_user_session(user_id)


        # ----------------------------------------------------
        # Run CareerGuide AI
        # ----------------------------------------------------

        result = Runner.run_sync(
            agent,
            request.message,
            context=context,
            session=session,
        )


        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return {
            "response": result.final_output,
            "user_id": user_id,
        }


    except Exception as error:

        print("ERROR:", error)

        return {
            "response": (
                "Sorry, I couldn't process your request right now."
            )
        }