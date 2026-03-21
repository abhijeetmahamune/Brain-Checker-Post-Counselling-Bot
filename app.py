from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pdf_utils import extract_text_from_pdf
from rag_pipeline import RAGPipeline
from llm_utils import generate_answer
import shutil
import os

app = FastAPI(title="Brain Checker Report Assistant")

rag = RAGPipeline()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Serve the chat frontend."""
    return FileResponse("index.html")


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = "uploaded.pdf"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)
    rag.chunk_text(text)
    rag.create_embeddings()

    return {"message": "PDF processed successfully"}


@app.post("/ask")
async def ask_question(request: dict):
    question = request.get("question", "")
    if not question:
        return {"error": "No question provided"}

    context = rag.retrieve(question)
    answer = generate_answer(context, question)

    return {"answer": answer}
