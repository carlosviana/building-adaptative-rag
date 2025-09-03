# Building Adaptive RAG System

An intelligent Retrieval-Augmented Generation (RAG) system that adaptively routes queries between vectorstore retrieval and web search using LangGraph workflows and Google Vertex AI.

## 🚀 Features

- **Adaptive Query Routing**: Intelligently routes questions to vectorstore or web search
- **Multi-Modal Retrieval**: Combines document retrieval with real-time web search
- **Document Grading**: Evaluates document relevance before generation
- **Hallucination Detection**: Validates generated responses for accuracy
- **Interactive CLI**: User-friendly command-line interface
- **Vertex AI Integration**: Powered by Google's Gemini models

## 🏗️ Architecture

The system uses a LangGraph workflow with the following components:

1. **Query Router**: Routes questions to appropriate data sources
2. **Document Retriever**: Fetches relevant documents from vectorstore
3. **Document Grader**: Evaluates document relevance
4. **Web Search**: Performs web search when needed
5. **Generator**: Creates responses using retrieved context
6. **Response Grader**: Validates response quality

## 📋 Prerequisites

- Python 3.10+
- Google Cloud Project with Vertex AI enabled
- Service Account with Vertex AI permissions
- Tavily API key (for web search)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd building-adaptative-rag
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Using uv (recommended)
   uv pip install -r requirements.txt
   ```

## ⚙️ Configuration

### 1. Google Vertex AI Setup

1. Create a Google Cloud Project
2. Enable Vertex AI API
3. Create a Service Account with Vertex AI User role
4. Download the service account JSON key
5. Place the JSON file as `vertex-ai-credentials.json` in the project root

### 2. Environment Variables

Create a `.env` file in the project root:

```env
# Vertex AI Credentials
GOOGLE_APPLICATION_CREDENTIALS=vertex-ai-credentials.json
PROJECT_ID=your-project-id
LOCATION=us-central1
GOOGLE_LLM_MODEL=gemini-2.5-flash
GOOGLE_EMBEDDINGS_MODEL=gemini-embedding-001

# Web Search (Required)
TAVILY_API_KEY=your-tavily-api-key

# LangChain Tracing (Optional)
LANGCHAIN_API_KEY=your-langchain-api-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=agentic-rag
```

### 3. API Keys

- **Tavily API**: Get your key from [Tavily](https://tavily.com/)
- **LangChain (Optional)**: Get your key from [LangSmith](https://smith.langchain.com/)

## 🚀 Usage

### Running the System

```bash
python -m src.cli.main
```

### Example Interaction

```
Adaptive RAG System
Type 'quit' to exit.

Question: What are the key components of an AI agent?
Processing...

Answer: Based on the retrieved documents, AI agents typically consist of several key components:

1. **Planning**: The ability to decompose complex tasks into smaller, manageable subgoals
2. **Memory**: Both short-term memory for learning within context and long-term memory for retaining information
3. **Tool Use**: The capability to call external APIs and interact with external tools
4. **Reflection**: Self-evaluation and self-criticism to improve performance

These components work together to enable agents to perform complex reasoning and task execution autonomously.

Question: What's the weather like today?
Processing...

Answer: I don't have access to real-time weather information in my knowledge base. Let me search the web for current weather conditions...

[System performs web search and returns current weather information]
```

## 📁 Project Structure

```
building-adaptative-rag/
├── src/
│   ├── cli/
│   │   └── main.py              # CLI interface
│   ├── data/
│   │   └── ingestion.py         # Document ingestion and vectorstore
│   ├── models/
│   │   └── model.py             # Vertex AI model configuration
│   └── workflow/
│       ├── chains/              # LangChain components
│       │   ├── answer_grader.py
│       │   ├── generation.py
│       │   ├── hallucination_grader.py
│       │   ├── retrieval_grader.py
│       │   └── router.py
│       ├── nodes/               # Workflow nodes
│       │   ├── generate.py
│       │   ├── grade_documents.py
│       │   ├── retrieve.py
│       │   └── web_search.py
│       ├── consts.py           # Constants
│       ├── graph.py            # LangGraph workflow
│       └── state.py            # Workflow state
├── tests/
├── chroma_langchain_db/        # Vector database
├── .env                        # Environment variables
├── requirements.txt            # Dependencies
├── vertex-ai-credentials.json  # Vertex AI credentials
└── README.md
```

## 🔧 Customization

### Adding New Documents

Modify the URLs in `src/data/ingestion.py`:

```python
urls = [
    "https://your-document-url-1.com",
    "https://your-document-url-2.com",
    # Add more URLs
]
```

### Adjusting Model Parameters

Edit `src/models/model.py` to change model settings:

```python
llm_model = ChatVertexAI(
    model_name=os.getenv("GOOGLE_LLM_MODEL"),
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION"),
    temperature=0.1,  # Adjust temperature
    max_tokens=1000,  # Set max tokens
)
```

### Modifying Routing Logic

Update the routing prompt in `src/workflow/chains/router.py`:

```python
system = """You are an expert at routing queries.
Route to vectorstore for: [your specific topics]
Route to web search for: [other topics]"""
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 📊 Monitoring

The system supports LangSmith tracing for monitoring and debugging:

1. Set up LangSmith account
2. Add your API key to `.env`
3. View traces at [LangSmith](https://smith.langchain.com/)

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Vertex AI Authentication**: Verify service account permissions
3. **API Rate Limits**: Check your Vertex AI quotas
4. **Memory Issues**: Reduce chunk size in document processing

### Debug Mode

Enable verbose logging by setting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the RAG framework
- [LangGraph](https://langgraph-sdk.vercel.app/) for workflow orchestration
- [Google Vertex AI](https://cloud.google.com/vertex-ai) for LLM capabilities
- [Tavily](https://tavily.com/) for web search functionality
- [Chroma](https://www.trychroma.com/) for vector storage

## 📞 Support

For questions and support, please open an issue in the repository or contact the maintainers.
