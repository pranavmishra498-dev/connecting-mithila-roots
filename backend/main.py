
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from services.rag_service import get_rag_answer


# 1. Create FastAPI application
app = FastAPI(
    title="Connecting Mithila Roots",
    description="AI-powered Mithila Knowledge Assistant",
    version="1.0.0"
)
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
# 2. Define request structure
class ChatRequest(BaseModel):

    question: str = Field(
        min_length=1,
        max_length=2000
    )


# 3. Home route
@app.get("/")
def home():

    return {
        "message": "Welcome to Connecting Mithila Roots!",
        "status": "Backend is running successfully"
    }


# 4. Health check route
@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# 5. AI chat endpoint
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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the AI answer."
        )
