
import traceback
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from supabase import create_client

from services.rag_service import get_rag_answer


# Load environment variables
load_dotenv()


# 1. Create FastAPI application
app = FastAPI(
    title="Connecting Mithila Roots",
    description="AI-powered Mithila Knowledge Assistant",
    version="1.0.0"
)


# 2. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. Chat request structure
class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000
    )


# 4. Story request structure
class StoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    location: str = Field(default="", max_length=150)
    category: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=5000)


# 5. Feedback request structure
class FeedbackRequest(BaseModel):
    name: str = Field(default="Anonymous", max_length=100)
    rating: int = Field(ge=1, le=5)
    message: str = Field(min_length=1, max_length=2000)


# 6. Supabase connection
def get_supabase_client():

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise HTTPException(
            status_code=500,
            detail="Supabase configuration is missing."
        )

    return create_client(supabase_url, supabase_key)


# 7. Home route
@app.get("/")
def home():

    return {
        "message": "Welcome to Connecting Mithila Roots!",
        "status": "Backend is running successfully"
    }


# 8. Health check route
@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# 9. AI chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    try:
        result = get_rag_answer(request.question)

        return {
            "success": True,
            "question": result["question"],
            "answer": result["answer"],
            "sources": result["sources"],
            "recommendation": result["recommendation"]
        }

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# 10. Submit Mithila story endpoint
@app.post("/submit-story")
def submit_story(request: StoryRequest):

    try:
        supabase = get_supabase_client()

        story_data = {
            "name": request.name.strip(),
            "location": request.location.strip(),
            "category": request.category,
            "message": request.message.strip()
        }

        supabase.table("mithila_stories").insert(
            story_data
        ).execute()

        return {
            "success": True,
            "message": "Your Mithila story has been submitted successfully!"
        }

    except HTTPException:
        raise

    except Exception:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Unable to submit your story. Please try again."
        )


# 11. Submit feedback endpoint
@app.post("/submit-feedback")
def submit_feedback(request: FeedbackRequest):

    try:
        supabase = get_supabase_client()

        feedback_data = {
            "name": request.name.strip() or "Anonymous",
            "rating": request.rating,
            "message": request.message.strip()
        }

        supabase.table("user_feedback").insert(
            feedback_data
        ).execute()

        return {
            "success": True,
            "message": "Thank you for your feedback!"
        }

    except HTTPException:
        raise

    except Exception:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Unable to submit feedback. Please try again."
        )