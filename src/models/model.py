import os
from dotenv import load_dotenv
from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings

load_dotenv()

# Set up Vertex AI credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

### chat model
llm_model = ChatVertexAI(
    model_name=os.getenv("GOOGLE_LLM_MODEL"),
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION"),
    temperature=0,
)

### embeddings model
embed_model = VertexAIEmbeddings(
    model_name=os.getenv("GOOGLE_EMBEDDINGS_MODEL"),
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION"),
)
