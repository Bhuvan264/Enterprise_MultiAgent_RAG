from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents.supervisor_agent import SupervisorAgent


app = FastAPI(
    title="Enterprise Multi-Agent RAG API",
    description="Backend API for the Enterprise Multi-Agent RAG System",
    version="1.0.0"
)


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# Serve Enterprise PDF Documents
# ==============================

app.mount(
    "/documents",
    StaticFiles(directory="data/documents"),
    name="documents"
)


# ==============================
# Supervisor Agent
# ==============================

supervisor = SupervisorAgent()


# ==============================
# Request Model
# ==============================

class QuestionRequest(BaseModel):
    question: str


# ==============================
# Root Endpoint
# ==============================

@app.get("/")
def root():

    return {
        "message": "Enterprise Multi-Agent RAG API is running",
        "status": "success"
    }


# ==============================
# Health Check
# ==============================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ==============================
# Ask Question
# ==============================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    print("\n==============================")
    print("API REQUEST")
    print("==============================")

    print(f"Question: {request.question}")

    result = supervisor.run(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }