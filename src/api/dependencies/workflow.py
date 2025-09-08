from dotenv import load_dotenv
from src.core.workflow.graph import get_workflow

# Load environment variables at startup
load_dotenv()

# Initialize workflow once at startup
workflow = get_workflow()

def get_workflow_dependency():
    return workflow
