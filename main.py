import os
import warnings

# Suppress Pydantic V1 compatibility warning on Python 3.14+
warnings.filterwarnings("ignore", message=".*Core Pydantic V1 functionality isn't compatible.*")

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables from .env file
load_dotenv()

# Check if variables are loaded
tracing = os.getenv("LANGSMITH_TRACING")
api_key = os.getenv("LANGSMITH_API_KEY")
hf_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

print(f"LANGSMITH_TRACING is set to: {tracing}")

if api_key and hf_api_key:
    # Print only first/last few chars for security
    masked_key = f"{api_key[:4]}...{api_key[-4:]}"
    hf_masked_key = f"{hf_api_key[:4]}...{hf_api_key[-4:]}"
    print(f"LANGSMITH_API_KEY is found: {masked_key}")
    print(f"HUGGINGFACEHUB_API_TOKEN is found: {hf_masked_key}")
else:
    print("LANGSMITH_API_KEY is NOT found.")
    print("HUGGINGFACEHUB_API_TOKEN is NOT found.")

model = init_chat_model(
    "qwen3:1.7b",
    model_provider="ollama",
    temperature=0.7,
    max_tokens=1024,
)

from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="qwen3:1.7b")

from langchain_core.vectorstores import InMemoryVectorStore

vector_store = InMemoryVectorStore(embeddings)

