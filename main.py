
from pathlib import Path
import os
import traceback

from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

load_dotenv()

# Import EduGenie modules
from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

# Initialize FastAPI
app = FastAPI(title="EduGenie")

# Static files and templates
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Request models
class TopicRequest(BaseModel):
    topic: str

class TextRequest(BaseModel):
    text: str

# Home page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

# Q&A
@app.get("/qa")
def answer_question(question: str = Query(...)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}

# Explanation
@app.post("/explain/")
def explain_api(data: TopicRequest):
    if not data.topic.strip():
        return {"error": "Please provide a topic."}

    explanation = explain_topic(data.topic)
    return {"topic": data.topic, "explanation": explanation}

# Summarization
@app.post("/summarize/")
def summarize_api(data: TextRequest):
    if not data.text.strip():
        return {"error": "Please provide text to summarize."}

    summary = summarize_text(data.text)
    return {"summary": summary}

# Quiz Generation
@app.post("/quiz/")
def quiz_api(data: TextRequest):
    if not data.text.strip():
        return {"error": "Please provide text for quiz."}

    quiz = generate_quiz(data.text)
    return {"quiz": quiz}

# Learning Recommendations
@app.get("/learning-path")
async def learning_path(topic: str = Query(...)):
    try:
        result = get_learning_recommendations(topic)
        return {"recommendation": result}

    except Exception as e:
        traceback.print_exc()
        error = str(e)

        if "429" in error or "RESOURCE_EXHAUSTED" in error:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Gemini API quota exceeded. Please try again later."
                }
            )

        return JSONResponse(
            status_code=500,
            content={"error": error}
        )