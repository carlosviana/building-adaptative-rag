from fastapi import APIRouter, Depends
from src.api.models.requests import ChatRequest
from src.api.models.responses import ChatResponse
from src.core.workflow_service import WorkflowService
from src.api.dependencies.workflow import get_workflow_dependency
import uuid

router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
def ask(
    request: ChatRequest,
    workflow = Depends(get_workflow_dependency)
):
    service = WorkflowService(workflow)
    response = service.run_workflow(request.question)
    
    # Generate session_id if not provided
    session_id = request.session_id or str(uuid.uuid4())
    response["session_id"] = session_id
    
    return ChatResponse(**response)
