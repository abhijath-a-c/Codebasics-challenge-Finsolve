# === data_processor.py ===

import os
import csv
from pathlib import Path
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BASE_DATA_DIR = Path(os.getenv("BASE_DATA_DIR"))
VECTORSTORE_DIR = Path(os.getenv("VECTORSTORE_DIR"))

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)

def format_csv_row(row: dict) -> str:
    return "\n".join(f"{key.strip()}: {value.strip()}" for key, value in row.items())

def process_csv_file(file_path: str, source_name: str) -> list:
    documents = []
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_text = format_csv_row(row)
            full_text = f"CSV Row from {source_name}:\n{row_text}"
            documents.append(Document(page_content=full_text, metadata={"source": source_name}))
    return documents

def process_folder(folder_path: str, persist_path: str):
    folder_path = Path(folder_path)
    persist_path = Path(persist_path)
    folder_name = folder_path.name

    logger.info(f"📂 Processing folder: {folder_path}")
    logger.info(f"📦 Persist path (Vector DB): {persist_path}")

    all_documents = []

    for file in folder_path.glob("*.md"):
        logger.info(f"➡️ Processing Markdown file: {file.name}")
        loader = UnstructuredMarkdownLoader(str(file))
        documents = loader.load()
        for doc in documents:
            doc.metadata["source"] = f"{folder_name} = {file.name}"
        split_documents = text_splitter.split_documents(documents)
        all_documents.extend(split_documents)
        logger.info(f"✅ Added '{file.name}' (markdown) to pending vector DB")

    for file in folder_path.glob("*.csv"):
        logger.info(f"➡️ Processing CSV file: {file.name}")
        formatted_documents = process_csv_file(str(file), f"{folder_name} = {file.name}")
        split_documents = text_splitter.split_documents(formatted_documents)
        all_documents.extend(split_documents)
        logger.info(f"✅ Added '{file.name}' (CSV) to pending vector DB")

    if not all_documents:
        logger.warning(f"⚠️ No documents found in folder: {folder_path}")
        return

    db = Chroma.from_documents(all_documents, embeddings, persist_directory=str(persist_path))
    logger.info(f"✅ Persisted vector store at: {persist_path}")

def process_all_folders():
    if not BASE_DATA_DIR.exists():
        raise FileNotFoundError(f"❌ Data folder not found: {BASE_DATA_DIR}")

    logger.info(f"🔎 Looking for folders inside: {BASE_DATA_DIR}")

    for folder in BASE_DATA_DIR.iterdir():
        if folder.is_dir():
            target_vectorstore_path = VECTORSTORE_DIR / folder.name
            logger.info(f"🛠 Processing department folder: {folder.name}")
            logger.info(f"📁 Target vector store path: {target_vectorstore_path}")

            target_vectorstore_path.mkdir(parents=True, exist_ok=True)
            process_folder(folder, target_vectorstore_path)

    logger.info("✅ Completed processing all department folders.")

if __name__ == "__main__":
    process_all_folders()
    print("✅ Data processing completed successfully.")
