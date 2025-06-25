# 🚀 FinSolve IQ: RAG-Based Internal Chatbot with Role-Based Access Control

Welcome to the **FinSolve Internal Chatbot** project!
This solution is designed to break down data silos and accelerate decision-making across Finance, Marketing, HR, Engineering, C-Level Executives, and Employees by providing secure, role-specific access to company knowledge.

---

## 🏢 Project Purpose

FinSolve Technologies, a leading FinTech company, recognized that delays in communication and fragmented data access were hindering productivity and strategic execution.
To address these challenges, this project implements a **Retrieval-Augmented Generation (RAG)** chatbot with **Role-Based Access Control (RBAC)**, ensuring every team member gets the right information, securely and instantly.

---

## 🛠️ Architecture Overview

![Architecture Diagram]([assets/architecture.png](https://mermaid.ink/img/pako:eNptk2lr4zAQhv_KoM9xmjptEpulkDuBBkrTdmHtUhRrYpvakqujx9b97yvZDWlgBQbPSO8zl_RJEsGQhGRfiLcko1LD3SzmYNc4ulcoH8HzrurfuIP7dQ2TaKsl0rLINSyk4Bo5-7WTVyY_W4kSu9UHUM6goimqM_9pmlFtfY8tcNKgbufbOxjfrMGDF4NK54I3GlMVgrIaptGCKu0OTGjy_M2nVXVW0pwfYdMWNl7CtUjzpIZZdIta5vhKC29s0hJtcgyWyFFSF-SAkTQ9UmYN5QETLSRskcokq2EeTTMpSgrf_tnEaV8bQ9kPYS8KZlvzkzEvd8hYzlNVwyJamTS1_wuaIBx3TgTX1xvXhhqW0VKKF3C2B65jzjypcpEXCDdSJKiU5dSwimZU04NLyENtzHqfqoP3WOaqwWzpK9oAhj_bHOcxb_eU2aWSVhk4ZOtyax1tqHxm4q2dznT7AC4N5UK5MKc9sGM68NYuFqxaY94E3qCmTmOH9LMDY67eUHoW722FkTZpO_2T6aKqBFdo793PG_Q_3TjmpENSmTMSammwQ0qU9sZYk3w6cUx0hiXGJLS_DPfUFDomMf-ysoryP0KUB6UUJs1IuKeFspapbOo4y6nt0vGILRjlVBiuSej7QcMg4Sd5t2Z_2B2MLnrD3vloMPT93rBDPkjo-V1_MAgugiDo9_xg1O9_dcjfJmyvG1yO3MawHwT-ef_yokOQ5faqbdrH2bzRr3_INSzh))
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

```bash
git clone https://github.com/your-org/FinSolve-Internal-Chatbot.git
cd FinSolve-Internal-Chatbot
```

### 2️⃣ Set Up Environment Variables

Create a `.env` file in the `app/` directory:

```env
GROQ_API_KEY=your_api_key_here
VECTORSTORE_FOLDER=absolute/path/to/Vector Store
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Generate Vector Stores

Run `python app/data_processor.py`
*(Automatically triggered if missing when backend starts)*

### 5️⃣ Start the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

### 6️⃣ Start the Streamlit Frontend

```bash
streamlit run ui/Home.py
```

### 7️⃣ Access the Chatbot

Visit [http://localhost:8501](http://localhost:8501)

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

## 📝 Key Features

* 🔑 **Role-Based Access Control (RBAC)**
* 🧠 **Retrieval-Augmented Generation (RAG)**
* 📌 **Source Referencing for Transparency**
* ⚙️ **Automatic Vector Store Creation**
* 📊 **Data Splitter for Quality Assurance**

---

## 🤝 Contributing

Pull requests and suggestions are welcome!
For questions, contact the **FinSolve Technologies engineering team**.

---

## 📄 License

MIT License

---

Empowering **FinSolve teams** with **secure**, **instant**, and **role-specific** knowledge.
