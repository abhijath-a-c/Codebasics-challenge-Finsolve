import os
from typing import Dict, List, Tuple, Any
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from transformers import AutoTokenizer
import numpy as np
from collections import deque
from app.data_processor import process_folder

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
vectorstore_folder = os.getenv("VECTORSTORE_DIR")
base_data_dir = os.getenv("BASE_DATA_DIR")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
DEFAULT_MODEL = "gemma2-9b-it"
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
CONTEXT_WINDOW_SIZE = 8192
RESERVED_FOR_PROMPT_AND_QUESTION = 1024
MAX_CONTEXT_TOKENS = CONTEXT_WINDOW_SIZE - RESERVED_FOR_PROMPT_AND_QUESTION

role_to_vector_dirs: Dict[str, List[str]] = {
    "finance": ["finance"],
    "marketing": ["marketing"],
    "hr": ["hr"],
    "engineering": ["engineering"],
    "c-level": ["finance", "marketing", "hr", "engineering"],
    "employee": ["general"]
}

def get_vector_dbs_for_role(user_role: str) -> List[Chroma]:
    selected_dirs = role_to_vector_dirs.get(user_role)
    if not selected_dirs:
        raise ValueError(f"Invalid role: {user_role}")

    vector_dbs = []
    for folder in selected_dirs:
        path = os.path.join(vectorstore_folder, folder)
        if os.path.exists(path):
            vector_dbs.append(Chroma(persist_directory=path, embedding_function=embeddings))

    if not vector_dbs:
        raise FileNotFoundError(f"No vector stores found for role: {user_role}")

    return vector_dbs

def prioritized_similarity_search(vector_dbs: List[Chroma], query: str, top_k: int = 10) -> List[Tuple[Document, float]]:
    all_results = []
    for db in vector_dbs:
        results = db.similarity_search_with_score(query, k=top_k * 2)
        all_results.extend(results)

    return sorted(all_results, key=lambda x: x[1])[:top_k]

def fit_context_window(query: str, doc_score_pairs: List[Tuple[Document, float]]) -> Tuple[str, List[Document]]:
    total_tokens = len(tokenizer.encode(query))
    selected_docs = []

    for doc, _ in doc_score_pairs:
        chunk_tokens = len(tokenizer.encode(doc.page_content))
        if total_tokens + chunk_tokens <= MAX_CONTEXT_TOKENS:
            selected_docs.append(doc)
            total_tokens += chunk_tokens
        else:
            break

    context = "\n\n".join(doc.page_content for doc in selected_docs)
    return context, selected_docs

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

class CustomRetrievalQAChain:
    def __init__(self, user_role: str, model: str = DEFAULT_MODEL, memory_limit: int = 5):
        self.vector_dbs = get_vector_dbs_for_role(user_role)
        self.llm = ChatGroq(model=model, groq_api_key=groq_api_key)
        self.prompt = ChatPromptTemplate.from_template("""
        You are FinSolve IQ, the official intelligent assistant of FinSolve Technologies.

        Use the provided context and chat history to answer the user's question as clearly as possible.
        If the context does not contain the answer, politely say: "I’m not sure about that from the available information."

        Context:
        {context}

        Chat History:
        {chat_history}

        User's Question:
        {question}
        """)
        self.chat_history = deque(maxlen=memory_limit)

    def invoke(self, inputs: Dict[str, str]) -> Dict[str, Any]:
        question = inputs.get("question", "").strip()
        if not question:
            raise ValueError("Question cannot be empty.")

        retrieved_docs_with_scores = prioritized_similarity_search(self.vector_dbs, query=question, top_k=10)
        context, selected_docs = fit_context_window(question, retrieved_docs_with_scores)

        chat_history_text = "\n".join(f"User: {q}\nAssistant: {a}" for q, a in self.chat_history)
        formatted_prompt = self.prompt.format(context=context, chat_history=chat_history_text, question=question)

        response = self.llm.invoke(formatted_prompt).content
        self.chat_history.append((question, response))

        # Calculate embedding similarity between answer and context chunks
        response_embedding = np.array(embeddings.embed_query(response))

        context_used = False
        similarity_threshold = 0.5
        for doc in selected_docs:
            chunk_embedding = np.array(embeddings.embed_query(doc.page_content))
            similarity = cosine_similarity(response_embedding, chunk_embedding)
            if similarity >= similarity_threshold:
                context_used = True
                break

        sources = []
        if context_used:
            for idx, doc in enumerate(selected_docs[:2]):  # Only include top 2 chunks
                dept_name = doc.metadata.get("source", "Unknown")
                sources.append({
                    "source": f"{dept_name} - chunk {idx+1}",
                    "content": doc.page_content
                })

        return {
            "answer": response,
            "sources": sources,
            "context_used": context_used
        }

def process_new_files(department: str):
    folder_path = os.path.join(base_data_dir, department)
    persist_path = os.path.join(vectorstore_folder, department)
    os.makedirs(persist_path, exist_ok=True)
    process_folder(folder_path, persist_path)
