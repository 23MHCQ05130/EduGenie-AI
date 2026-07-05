from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

from backend.gemini_service import ask_gemini
from backend.quiz import generate_quiz
from backend.summary import summarize_text
from backend.roadmap import generate_roadmap
from backend.pdf_reader import extract_text_from_pdf

app = FastAPI(
    title="EduGenie AI",
    description="AI Powered Educational Assistant",
    version="3.0"
)

# ==========================================
# Static Files & Templates
# ==========================================

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ==========================================
# In-Memory Storage
# ==========================================

chat_history = []

stats = {
    "questions": 0,
    "quiz": 0,
    "summary": 0,
    "roadmap": 0,
    "pdf": 0
}

# ==========================================
# Page Routes
# ==========================================

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


@app.get("/ask-page")
def ask_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="ask.html"
    )


@app.get("/quiz-page")
def quiz_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="quiz.html"
    )


@app.get("/summary-page")
def summary_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="summary.html"
    )


@app.get("/roadmap-page")
def roadmap_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="roadmap.html"
    )


@app.get("/history")
def history(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="history.html"
    )


# ==========================================
# Request Models
# ==========================================

class Question(BaseModel):
    question: str


class QuizRequest(BaseModel):
    topic: str
    difficulty: str
    num_questions: int


class SummaryRequest(BaseModel):
    text: str


class RoadmapRequest(BaseModel):
    topic: str


# ==========================================
# Ask AI API
# ==========================================

@app.post("/ask")
def ask(question: Question):

    answer = ask_gemini(question.question)

    stats["questions"] += 1

    chat_history.append({
        "question": question.question,
        "answer": answer
    })

    return {
        "answer": answer
    }


# ==========================================
# Quiz API
# ==========================================

@app.post("/quiz")
def quiz(request: QuizRequest):

    quiz = generate_quiz(
        request.topic,
        request.difficulty,
        request.num_questions
    )

    stats["quiz"] += 1

    return {
        "quiz": quiz
    }


# ==========================================
# Summary API
# ==========================================

@app.post("/summary")
def summary(request: SummaryRequest):

    summary = summarize_text(request.text)

    stats["summary"] += 1

    return {
        "summary": summary
    }


# ==========================================
# Roadmap API
# ==========================================

@app.post("/roadmap")
def roadmap(request: RoadmapRequest):

    roadmap = generate_roadmap(request.topic)

    stats["roadmap"] += 1

    return {
        "roadmap": roadmap
    }


# ==========================================
# PDF Upload API
# ==========================================

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    extracted_text = extract_text_from_pdf(file_path)

    if extracted_text.strip() == "":
        return {
            "summary": "No readable text found in the PDF."
        }

    summary = summarize_text(extracted_text)

    stats["pdf"] += 1

    return {
        "summary": summary
    }


# ==========================================
# Dashboard Statistics API
# ==========================================

@app.get("/stats")
def get_stats():
    return stats


# ==========================================
# Chat History API
# ==========================================

@app.get("/chat-history")
def get_chat_history():
    return {
        "history": chat_history
    }