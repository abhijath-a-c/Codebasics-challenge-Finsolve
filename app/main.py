import os
import logging
from typing import Dict
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
import subprocess
import shutil

from app.rag import CustomRetrievalQAChain, role_to_vector_dirs, process_new_files

load_dotenv()

BASE_DATA_DIR = os.getenv("BASE_DATA_DIR")
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR")

app = FastAPI()
security = HTTPBasic()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"},
    "Clark": {"password": "superman", "role": "c-level"},
    "General": {"password": "general123", "role": "employee"}
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}

class ChatRequest(BaseModel):
    question: str

@app.on_event("startup")
def process_vectorstore():
    try:
        subprocess.run(["python", "app/data_processor.py"], check=True)
    except Exception as e:
        logger.exception("Error processing vectorstore on startup")

@app.post("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}

@app.post("/chat")
def chat(request: ChatRequest, user=Depends(authenticate)):
    try:
        qa_chain = CustomRetrievalQAChain(user_role=user['role'])
        result = qa_chain.invoke({"question": request.question})
        return {
            "answer": result["answer"],
            "sources": result.get("sources", []),
            "context_used": result.get("context_used", [])
        }
    except Exception:
        logger.exception("Error during chat generation")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    target_department: str = Form(...),
    user=Depends(authenticate)
):
    if target_department not in role_to_vector_dirs:
        raise HTTPException(status_code=400, detail="Invalid department")

    if user['role'] != "c-level" and target_department != user['role']:
        raise HTTPException(status_code=403, detail="Permission denied for this department")

    target_folder = os.path.join(BASE_DATA_DIR, target_department)
    os.makedirs(target_folder, exist_ok=True)

    file_path = os.path.join(target_folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_new_files(target_department)

    return {"message": f"✅ File '{file.filename}' uploaded and processed successfully to {target_department}."}

@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}!", "role": user["role"]}
