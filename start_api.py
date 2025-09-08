#!/usr/bin/env python3
"""
Script para inicializar a API REST do sistema RAG Adaptativo
"""
import os
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas"""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI e Uvicorn encontrados")
        return True
    except ImportError:
        print("❌ FastAPI ou Uvicorn não encontrados")
        print("Execute: pip install fastapi uvicorn")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe"""
    env_path = Path(".env")
    if env_path.exists():
        print("✅ Arquivo .env encontrado")
        return True
    else:
        print("❌ Arquivo .env não encontrado")
        print("Crie um arquivo .env com as variáveis necessárias")
        return False

def start_api():
    """Inicia a API REST"""
    print("🚀 Iniciando API REST...")
    try:
        # Comando para iniciar a API com Uvicorn
        subprocess.run([
            "uvicorn", 
            "src.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar a API: {e}")
        return False
    except FileNotFoundError:
        print("❌ Comando 'uvicorn' não encontrado")
        print("Certifique-se de que o Uvicorn está instalado corretamente")
        return False
    
    return True

def main():
    """Função principal"""
    print("🔧 Configurando API REST para RAG Adaptativo")
    print("=" * 50)
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Verificar arquivo .env
    if not check_env_file():
        print("\nCrie um arquivo .env com as seguintes variáveis:")
        print("""
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
        """)
        sys.exit(1)
    
    print("✅ Todas as verificações passaram!")
    print("\n🌐 A API será iniciada em: http://localhost:8000")
    print("📊 Documentação automática em: http://localhost:8000/docs")
    print("🔍 Endpoint principal: POST /api/v1/chat/ask")
    
    # Iniciar a API
    start_api()

if __name__ == "__main__":
    main()
