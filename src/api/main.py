from fastapi import FastAPI
from src.api.routes import chat

app = FastAPI()

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/api/v1/health", tags=["health"])
def health():
    return {"status": "ok"}