#!/usr/bin/env python3
"""
Script para inicializar o LangGraph Studio para o projeto RAG Adaptativo
"""
import os
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas"""
    try:
        import langgraph_studio
        print("✅ LangGraph Studio encontrado")
        return True
    except ImportError:
        print("❌ LangGraph Studio não encontrado")
        print("Execute: pip install langgraph-studio")
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

def start_studio():
    """Inicia o LangGraph Studio"""
    print("🚀 Iniciando LangGraph Studio...")
    try:
        # Comando para iniciar o LangGraph Studio
        subprocess.run(["langgraph", "studio"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar o Studio: {e}")
        return False
    except FileNotFoundError:
        print("❌ Comando 'langgraph' não encontrado")
        print("Certifique-se de que o LangGraph Studio está instalado corretamente")
        return False
    
    return True

def main():
    """Função principal"""
    print("🔧 Configurando LangGraph Studio para RAG Adaptativo")
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
    
    # Verificar se langgraph.json existe
    if not Path("langgraph.json").exists():
        print("❌ Arquivo langgraph.json não encontrado")
        sys.exit(1)
    
    print("✅ Todas as verificações passaram!")
    print("\n🌐 O LangGraph Studio será aberto em: http://localhost:8123")
    print("📊 Você poderá visualizar e debugar o grafo RAG adaptativo")
    
    # Iniciar o Studio
    start_studio()

if __name__ == "__main__":
    main()
