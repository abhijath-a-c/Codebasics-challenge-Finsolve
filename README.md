# 🚀 FinSolve IQ: RAG-Based Internal Chatbot with Role-Based Access Control

Welcome to the **FinSolve Internal Chatbot** project!
This solution is designed to break down data silos and accelerate decision-making across Finance, Marketing, HR, Engineering, C-Level Executives, and Employees by providing secure, role-specific access to company knowledge.

Check [Codebasics Project Challenge](https://codebasics.io/challenge/codebasics-gen-ai-data-science-resume-project-challenge#current_challenge)

---

## 🏢 Project Purpose

A Q&A chatbot that retrieve information from company's internal data.<br>
Department specific access to data

---

## 🛠️ Architecture Overview

![Architecture Diagram](https://github.com/abhijath-a-c/Codebasics-challenge-Finsolve/blob/main/readme_image/architecture.png)
---

## 🖥️ Features Overview

| Component                 | Description                                                |
| ------------------------- | ---------------------------------------------------------- |
| **Streamlit UI**          | User-friendly chat interface for login and queries         |
| **FastAPI Backend**       | Handles authentication, role assignment, and API endpoints |
| **RBAC Module**           | Ensures users access only data permitted by their role     |
| **RAG Pipeline**          | Retrieves relevant documents and augments LLM responses    |
| **Vector Store (Chroma)** | Stores department-specific document embeddings             |
| **LLM (Groq/Gemma)**      | Generates context-rich, natural language answers           |

---

## 🧩 Code Structure & Key Components

| File / Folder           | Purpose                                                     |
| ----------------------- | ----------------------------------------------------------- |
| `app/main.py`           | FastAPI backend: authentication, RBAC, `/chat` endpoint     |
| `app/rag.py`            | RAG pipeline: role-based vector retrieval, prompt creation  |
| `app/data_processor.py` | Loads documents, generates embeddings, builds vector stores |
| `ui/Home.py`            | Streamlit UI: login, chat interface, session management     |
| `Vector Store/`         | Stores Chroma vector databases for each department          |

---

## 🔑 Roles & Permissions

| Role            | Data Access                                                           |
| --------------- | --------------------------------------------------------------------- |
| **Finance**     | Financial reports, expenses, reimbursements, etc.                     |
| **Marketing**   | Campaign performance, customer feedback, sales metrics                |
| **HR**          | Employee data, attendance, payroll, performance reviews               |
| **Engineering** | Technical architecture, development processes, operational guidelines |
| **C-Level**     | **Full access to all company data**                                   |
| **Employee**    | General company info: policies, events, FAQs                          |

---

## 🚦 How It Works

1️⃣ User logs in via Streamlit UI (username/password)  
2️⃣ FastAPI backend authenticates and determines the user's role  
3️⃣ RAG pipeline retrieves relevant documents from the vector store based on role  
4️⃣ LLM generates a context-rich answer, referencing source documents  
5️⃣ Response is returned to the user, ensuring secure, role-based access  

---

## 🏃 How to Run the Project

### 1️⃣ Clone the Repository

```CMD
git clone "link "

```

### 2️⃣ Set Up Environment Variables

Create a `.env` file in the `app/` directory:

```env
GROQ_API_KEY=your_api_key_here
HF_TOKEN= your_huggingface token_here
VECTORSTORE_DIR=absolute/path/to/Vector Store
BASE_DATA_DIR=absolute/path/to/data
```

### 3️⃣ Create environment and Install Dependencies

```bash
conda create -p "environmentname" Python==3.10 
pip install -r requirements.txt
```

### 4️⃣ Generate Vector Stores

Run `python app/data_processor.py`
*(Automatically triggered if missing when backend starts)*

### 5️⃣ Start the FastAPI Backend

```CMD
uvicorn app.main:app --reload
```

### 6️⃣ Start the Streamlit Frontend

```CMD
streamlit run ui/Home.py
```

### 7️⃣ Access the Chatbot
Visit [http://localhost:8501](http://localhost:8501)


---

## 📝 Key Features

* 🔑 **Role-Based Access Control (RBAC)**
* 🧠 **Retrieval-Augmented Generation (RAG)**
* 📌 **Source Referencing for Transparency**
* ⚙️ **Automatic Vector Store Creation**
* 📊 **Data Splitter for Quality Assurance**
* 🖥️ **New Doc(.md/.csv) Upload from UI**
---


