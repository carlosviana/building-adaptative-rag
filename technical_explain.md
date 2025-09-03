# Sistema RAG Adaptativo - Documentação Técnica

## Arquitetura do Sistema

O sistema implementa um workflow baseado em grafos usando LangGraph, onde cada componente tem responsabilidades específicas e bem definidas. A arquitetura segue o padrão de **Retrieval-Augmented Generation (RAG)** com roteamento adaptativo e validação em múltiplas camadas.

## Conceitos Fundamentais

### Chains vs Nodes vs Routes

#### **Chains (Cadeias)**
```python
# Exemplo de uma chain simples
generation_chain = prompt | llm | parser
```

**Definição:** Uma sequência linear de componentes onde a saída de um é a entrada do próximo.

**Características:**
- Fluxo estritamente linear (A → B → C)
- Sem estado compartilhado
- Reutilizáveis e composáveis
- Focadas em uma tarefa específica

**Exemplo no Projeto:**
```python
# src/workflow/chains/answer_grader.py
answer_grader: RunnableSequence = answer_prompt | structured_llm_grader
```

#### **Nodes (Nós)**
```python
def retrieve(state: GraphState) -> Dict[str, Any]:
    """Retrieve documents from vector store."""
    print("---RETRIEVE---")
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}
```

**Definição:** Funções que operam sobre um estado compartilhado (GraphState) e executam uma etapa específica do workflow.

**Características:**
- Recebem o estado completo do grafo
- Leem informações necessárias do estado
- Executam lógica (frequentemente usando chains)
- Retornam atualizações para o estado compartilhado
- Permitem lógica condicional e loops

**Diferença Crucial:**
- **Chain:** `input → processing → output`
- **Node:** `state → read → process → update_state`

#### **Routes (Roteamento)**
```python
def decide_to_generate(state):
    """Route to web search or generation"""
    return WEBSEARCH if state["web_search"] else GENERATE
```

**Definição:** Funções que determinam o próximo nó a ser executado baseado no estado atual.

**Características:**
- Implementam lógica condicional
- Analisam o estado atual
- Retornam o nome do próximo nó
- Permitem fluxos não-lineares

## Componentes Técnicos Detalhados

### 1. Estado do Grafo (GraphState)

```python
# src/workflow/state.py
class GraphState(TypedDict):
    """State object for workflow containing query, documents and control flags."""
    question: str           # User query
    generation: str         # LLM-generated response
    web_search: bool       # Control flag for web search
    documents: List[str]   # Retrieved documents context
```

**Função:** Memória compartilhada que persiste informações entre nós.

**Design Pattern:** Typed Dictionary para type safety e documentação automática.

### 2. Chains Especializadas

#### **Router Chain**
```python
# src/workflow/chains/router.py
class RouteQuery(BaseModel):
    datasource: Literal["vectorstore", "websearch"] = Field(
        description="Route to web search or vectorstore"
    )

question_router: RunnableSequence = route_prompt | structured_llm_router
```

**Função:** Determina a fonte de dados mais apropriada para uma query.

**Técnica:** Structured Output com Pydantic para garantir outputs válidos.

#### **Grading Chains**
```python
# src/workflow/chains/answer_grader.py
class GradeAnswer(BaseModel):
    binary_score: bool = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

answer_grader: RunnableSequence = answer_prompt | structured_llm_grader
```

**Função:** Avalia qualidade e relevância de documentos/respostas.

**Pattern:** Binary classification com structured output.

### 3. Nós de Processamento

#### **Retrieve Node**
```python
def retrieve(state: GraphState) -> Dict[str, Any]:
    """Retrieve documents from vector store."""
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}
```

**Responsabilidades:**
- Extrai query do estado
- Invoca retriever (chain) para buscar documentos
- Atualiza estado com documentos encontrados

**Interoperação:** Usa a chain `retriever` definida em `data/ingestion.py`

#### **Grade Documents Node**
```python
def grade_documents(state: GraphState) -> Dict[str, Any]:
    """Grade document relevance and set web_search flag."""
    question = state["question"]
    documents = state["documents"]
    
    filtered_docs = []
    web_search = "No"
    
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        if score.binary_score == "yes":
            filtered_docs.append(d)
        else:
            web_search = "Yes"
    
    return {"documents": filtered_docs, "web_search": web_search}
```

**Responsabilidades:**
- Avalia relevância de cada documento
- Filtra documentos irrelevantes
- Define flag para busca web se necessário

**Pattern:** Filter-Map operation com side effects no estado.

#### **Generate Node**
```python
def generate(state: GraphState) -> Dict[str, Any]:
    """Generate answer using retrieved documents."""
    question = state["question"]
    documents = state["documents"]
    
    generation = generation_chain.invoke(
        {"context": documents, "question": question}
    )
    
    return {"documents": documents, "question": question, "generation": generation}
```

**Responsabilidades:**
- Combina documentos em contexto
- Gera resposta usando LLM
- Preserva estado anterior

### 4. Workflow Graph Construction

```python
# src/workflow/graph.py
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

# Define entry point with routing
workflow.set_conditional_entry_point(
    route_question,
    {WEBSEARCH: WEBSEARCH, RETRIEVE: RETRIEVE}
)

# Add conditional edges
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {WEBSEARCH: WEBSEARCH, GENERATE: GENERATE},
)
```

**Padrões Implementados:**
- **Conditional Entry Point:** Roteamento inicial baseado na query
- **Conditional Edges:** Decisões dinâmicas baseadas no estado
- **Linear Edges:** Fluxo determinístico entre nós

## Fluxos de Execução

### Fluxo 1: Vectorstore → Generate
```
User Query → Route Question → RETRIEVE → Grade Documents → GENERATE → End
```

### Fluxo 2: Vectorstore → Web Search → Generate
```
User Query → Route Question → RETRIEVE → Grade Documents → WEBSEARCH → GENERATE → End
```

### Fluxo 3: Direct Web Search
```
User Query → Route Question → WEBSEARCH → GENERATE → End
```

## Integração com Vertex AI

### Model Configuration
```python
# src/models/model.py
llm_model = ChatVertexAI(
    model_name=os.getenv("GOOGLE_LLM_MODEL"),
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION"),
    temperature=0,
)

embed_model = VertexAIEmbeddings(
    model_name=os.getenv("GOOGLE_EMBEDDINGS_MODEL"),
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION"),
)
```

**Authentication Pattern:** Service Account JSON com variáveis de ambiente.

**Models Used:**
- **LLM:** `gemini-2.5-flash` para geração de texto
- **Embeddings:** `gemini-embedding-001` para vetorização

## Vector Store Implementation

```python
# src/data/ingestion.py
def create_vectorstore():
    chroma_path = "./chroma_langchain_db"
    
    if os.path.exists(chroma_path):
        # Load existing
        vectorstore = Chroma(
            persist_directory=chroma_path,
            embedding_function=embed_model,
            collection_name="rag-chroma"
        )
    else:
        # Create new
        docs = [WebBaseLoader(url).load() for url in urls]
        doc_splits = text_splitter.split_documents(docs)
        
        vectorstore = Chroma.from_documents(
            documents=doc_splits,
            embedding=embed_model,
            persist_directory=chroma_path,
            collection_name="rag-chroma"
        )
    
    return vectorstore.as_retriever()
```

**Design Decisions:**
- **Lazy Loading:** Vectorstore criado apenas quando necessário
- **Persistence:** Dados salvos localmente para reutilização
- **Chunking Strategy:** RecursiveCharacterTextSplitter com 200 tokens

## Error Handling e Resilience

### Graceful Degradation
```python
def grade_generation_grounded_in_documents_and_questions(state):
    try:
        score = hallucination_grader.invoke({...})
        return "useful" if score.binary_score else "not useful"
    except Exception as e:
        logging.error(f"Grading failed: {e}")
        return "not useful"  # Fail safe
```

### Retry Logic
- Implementado através de conditional edges
- Loop back para regeneração em caso de respostas inadequadas
- Limite máximo de tentativas para evitar loops infinitos

## Performance Considerations

### Caching Strategy
- **Vector Store:** Persistido localmente (Chroma)
- **Model Responses:** Não cached (para freshness)
- **Web Search:** Rate limiting através da API Tavily

### Optimization Techniques
- **Batch Processing:** Múltiplos documentos avaliados em paralelo
- **Lazy Loading:** Componentes inicializados sob demanda
- **Memory Management:** Estado mínimo necessário

## Monitoring e Observability

### LangSmith Integration
```python
# Configurado via .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-key
LANGCHAIN_PROJECT=agentic-rag
```

**Métricas Coletadas:**
- Latência por nó
- Taxa de sucesso de cada chain
- Distribuição de rotas tomadas
- Qualidade das avaliações

### Logging Strategy
```python
print("---RETRIEVE---")  # Node entry logging
print("---DECISION: GENERATE---")  # Route decision logging
```

## Extensibilidade

### Adding New Nodes
1. Definir função que recebe `GraphState`
2. Implementar lógica específica
3. Retornar dicionário para atualizar estado
4. Adicionar ao workflow graph

### Adding New Chains
1. Criar em `src/workflow/chains/`
2. Definir Pydantic models para structured output
3. Compor prompt + LLM + parser
4. Usar em nós conforme necessário

### Custom Routing Logic
```python
def custom_route(state: GraphState) -> str:
    # Implement custom logic
    if condition:
        return "NODE_A"
    else:
        return "NODE_B"

workflow.add_conditional_edges(
    SOURCE_NODE,
    custom_route,
    {"NODE_A": node_a, "NODE_B": node_b}
)
```

## Security Considerations

### Data Privacy
- Documentos internos permanecem no vector store local
- Queries não são logadas em serviços externos
- Credenciais isoladas em variáveis de ambiente

### API Security
- Service Account com permissões mínimas
- Rate limiting em APIs externas
- Sanitização de inputs do usuário

---

*Esta arquitetura fornece uma base sólida e extensível para sistemas RAG complexos, balanceando performance, maintainability e scalability.*
