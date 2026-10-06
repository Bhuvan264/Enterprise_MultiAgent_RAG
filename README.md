# Enterprise Multi-Agent RAG

An enterprise document assistant built with a multi-agent architecture for retrieving, summarizing, and answering questions from company PDFs and policy documents.

This project combines:
- FastAPI backend for serving Q&A requests
- React frontend for chat-based interaction
- ChromaDB vector storage for semantic document retrieval
- LangChain + Ollama for embeddings and LLM-based answer generation
- Supervisor-driven agent routing for summary, document lookup, and RAG workflows

## Overview

The application accepts natural-language questions such as:
- "What is the remote work policy?"
- "Summarize the remote work policy."
- "Which document contains the remote work policy?"

The system then:
1. Routes the query to the appropriate agent
2. Retrieves relevant chunks from the document vector store
3. Uses an LLM to answer based only on retrieved context
4. Returns answer text and source references

## Architecture

- `api/main.py` — FastAPI application entrypoint
- `agents/` — agent logic for routing and specialized tasks
- `rag/` — retrieval, embedding, and QA pipeline
- `data/documents/` — source PDFs/document files
- `vectorstore/chroma_db/` — persistent ChromaDB vector database
- `frontend/` — React + Vite application UI

## Features

- Multi-agent query routing
- RAG-based semantic retrieval over enterprise documents
- Summary requests handled by a dedicated summary workflow
- Document lookup for identifying supporting PDFs
- Chat interface for end-user querying
- Source-aware answers with page-level document references

## Tech Stack

- Python
- FastAPI
- React
- Vite
- ChromaDB
- LangChain
- Ollama

## Prerequisites

Before running the app, make sure you have:
- Python 3.10+
- Node.js 18+
- npm
- Ollama installed locally

You will also need the following Ollama models pulled:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

## Project Structure

```text
Enterprise_MultiAgent_RAG/
├── agents/
│   ├── document_agent.py
│   ├── rag_agent.py
│   ├── summary_agent.py
│   ├── supervisor_agent.py
│   └── __init__.py
├── api/
│   ├── __init__.py
│   └── main.py
├── data/
│   └── documents/
├── frontend/
│   ├── package.json
│   ├── public/
│   ├── src/
│   ├── vite.config.js
│   └── README.md
├── rag/
│   ├── chunker.py
│   ├── embeddings.py
│   ├── loader.py
│   ├── qa.py
│   ├── retriever.py
│   ├── vectorstore.py
│   └── __init__.py
├── vectorstore/
│   └── chroma_db/
├── .gitignore
├── README.md
└── venv/
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Enterprise_MultiAgent_RAG
```

### 2. Activate the Python environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Python dependencies

If needed, install the required libraries:

```bash
pip install fastapi uvicorn chromadb langchain-ollama pydantic
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
```

## Running the Application

### Start the backend API

From the project root:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/health

### Start the frontend

In a separate terminal:

```bash
cd frontend
npm run dev
```

The React app will typically run on:
- http://localhost:5173

## Example Usage

Open the frontend in the browser and ask questions like:

- What is the remote work policy?
- Summarize the remote work policy.
- Which document contains the remote work policy?

The assistant will return a response and list supporting document sources.

## Notes

- The system expects enterprise PDFs or policy documents to be stored in `data/documents/`.
- The vector database is stored under `vectorstore/chroma_db/` and can be rebuilt or refreshed when new documents are added.
- If new documents are added, the embeddings/index should be regenerated using the project’s ingestion pipeline.

## License

This project is provided as a local development example for enterprise document retrieval and Q&A workflows.

## Contact / Contribution

For local development and experimentation, use this project as a starting point for building more advanced multi-agent retrieval systems with custom documents, policies, and internal knowledge sources.
