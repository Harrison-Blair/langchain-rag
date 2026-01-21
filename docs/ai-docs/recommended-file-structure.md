rag-agent/
│
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── document_processor.py       # File upload & processing logic
│   │   ├── embeddings. py              # Vector embeddings generation
│   │   ├── vector_store.py             # Vector database operations
│   │   ├── retriever.py                # Document retrieval logic
│   │   └── llm_interface.py            # LLM API interactions
│   │
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py              # Main GUI window (tkinter/PyQt/Streamlit)
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── file_uploader.py        # File upload widget
│   │   │   ├── chat_interface.py       # Chat display widget
│   │   │   └── settings_panel.py       # Settings/config widget
│   │   └── assets/
│   │       ├── icons/
│   │       └── styles. css              # GUI styling
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── terminal_interface.py       # CLI main interface
│   │   └── commands. py                 # CLI command handlers
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py                   # Configuration management
│       ├── logger.py                   # Logging setup
│       └── validators.py               # Input validation
│
├── data/
│   ├── uploads/                        # User-uploaded files
│   ├── vectorstore/                    # Persisted vector database
│   └── cache/                          # Temporary/cache files
│
├── config/
│   ├── default_config.yaml             # Default configuration
│   └── . env. example                    # Environment variables template
│
├── tests/
│   ├── __init__.py
│   ├── test_document_processor.py
│   ├── test_retriever.py
│   └── test_llm_interface.py
│
├── scripts/
│   ├── build_executable.py             # PyInstaller build script
│   └── setup_environment.sh            # Initial setup script
│
├── docs/
│   ├── USER_GUIDE.md
│   └── ARCHITECTURE.md
│
├── main.py                             # Single entry point launcher
├── requirements.txt                    # Python dependencies
├── pyproject.toml                      # Modern Python project config
├── README.md
├── . gitignore
└── LICENSE