# langchain-rag
RAG agent based on the [LangChain tutorial](https://docs.langchain.com/oss/python/langchain/rag) documentation. You can find the results of that tutorial in `example.py`.

# Setup
## Ollama Model
Pull the model
```
ollama pull qwen3:1.7b
```

Pull embeddings
```
ollama pull nomic-embed-text
```

## `.env` File
Copy `.env.example`, name it `.env`. Fill out the empty API keys.

## Virtual Enviornment
### Windows
Create virtual enviornment
```
py -3.13 -m venv .venv
```

Activate virtual enviornment
```
.\.venv\Scripts\activate
```

Install Requirements
```
pip install -r requirements.txt
```
### Ubuntu
Create Virtual enviornment
```
python -m venv .venv
```

Activate virtual enviornment
```
source .\.venv\bin\activate
```

Install Requirements
```
pip install -r requirements.txt
```
