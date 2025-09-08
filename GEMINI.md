# Gemini Project Overview: Adaptive RAG System

## 1. Project Goal

This project implements an adaptive Retrieval-Augmented Generation (RAG) system. It uses a LangGraph workflow to intelligently route user queries between a local vector database for internal knowledge and a web search for real-time or external information. The system evaluates the quality of retrieved information before generating a final, grounded answer.

## 2. Core Technologies

- **Orchestration**: LangGraph
- **API**: FastAPI
- **LLM & Embeddings**: Google Vertex AI (Gemini Pro, Gemini Flash)
- **Vector Store**: ChromaDB (local persistence)
- **Web Search**: Tavily Search API
- **Core Framework**: LangChain
- **CLI**: Python `argparse`

## 3. Architecture Overview

The architecture is designed with a clear separation of concerns, with a dedicated API layer, a service layer for business logic, and a core layer for the workflow itself.

- **API Layer (`src/api`)**: Handles HTTP requests, validation, and serialization. It's built with FastAPI.
- **Service Layer (`src/core/workflow_service.py`)**: Encapsulates the business logic of running the workflow, handling sessions, and formatting the output.
- **Core Workflow Layer (`src/core/workflow`)**: Contains the LangGraph workflow definition, including nodes, chains, and the graph itself. This layer is independent of the API and can be used in other contexts (e.g., the CLI).

## 4. Key Files & Directories

```
C:/Users/carlos.viana/learn/agents_flow/building-adaptative-rag/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app + startup
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── chat.py          # Chat endpoints
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── requests.py      # Pydantic request models
│   │   │   └── responses.py     # Pydantic response models
│   │   └── dependencies/
│   │       ├── __init__.py
│   │       └── workflow.py      # Workflow injection
│   ├── cli/                     # Existing CLI
│   │   └── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── workflow_service.py  # Service layer
│   │   ├── models.py            # Pydantic models for the core layer
│   │   └── workflow/            # LangGraph workflow
│   │       ├── chains/
│   │       ├── nodes/
│   │       ├── consts.py
│   │       ├── graph.py
│   │       └── state.py
│   └── data/                    # Data ingestion
│       └── ingestion.py
├── requirements.txt             # Project dependencies.
└── .env                         # For storing API keys and environment variables.
```

## 5. Configuration & Setup

1.  **Install Dependencies**: `pip install -r requirements.txt`
2.  **Environment Variables**: Create a `.env` file in the root directory with the following keys:
    - `GOOGLE_APPLICATION_CREDENTIALS`: Path to the Google Cloud service account JSON file (e.g., `vertex-ai-credentials.json`).
    - `PROJECT_ID`: Your Google Cloud Project ID.
    - `LOCATION`: The Google Cloud region (e.g., `us-central1`).
    - `TAVILY_API_KEY`: Your API key for Tavily search.
    - `LANGCHAIN_API_KEY` (Optional): For tracing with LangSmith.

## 6. How to Run

### API

-   To run the FastAPI server, execute the following command from the project root:
    ```bash
    uvicorn src.api.main:app --reload
    ```
-   The API will be available at `http://127.0.0.1:8000`. You can access the interactive documentation at `http://127.0.0.1:8000/docs`.

### CLI

-   To run the interactive command-line interface, execute the following command from the project root:
    ```bash
    python -m src.cli.main
    ```
