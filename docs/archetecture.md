# Archetecture
General app architecture for the RAG agent application

## Tooling/Libraries
- LLM running w/ `Ollama`
- LLM middleware w/ `LangChain`
    - Diagnostics w/ `LangSmith`
- PDF text extraction w/ `PyMuPDF`

- UI interface w/ `Rich` & `Textual`

## Workflow

Get Docs -> Process Docs -> Vector Store

Load Model -> Load Embeddings -> Get Tools -> Create Agent

Created Agent
 - Prompt -> Search For Context -> Respond

Tools:
 - Search Vector Store
 - Determine Prompt?