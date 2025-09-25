# M2-Semantic-Engine

A **modular, high-performance semantic engine** for large-scale natural-language understanding and retrieval-augmented reasoning (RAG).  
This repository provides a complete pipeline—**ingestion → embeddings → indexing → retrieval → reasoning → API**—ready for production or research.

---

## License

![Apache 2.0 License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)  
![Dual License](https://img.shields.io/badge/License-Dual%20License-green?style=flat-square) 

This project is **dual-licensed**:

- **Open-Source / Personal Use:** Apache 2.0  
- **Commercial / Closed-Source Use:** Proprietary license required 

For commercial licensing inquiries or enterprise use, please contact: [mahbub.aaman.app@gmail.com](mailto:mahbub.aaman.app@gmail.com)


## High-Level Architecture

The diagram below shows how components communicate from raw data to API response.

```
                ┌─────────────────────────┐
                │        Client / UI      │
                │  (Web App / CLI / API)  │
                └───────────┬─────────────┘
                            │  REST / gRPC
                            ▼
                ┌─────────────────────────┐
                │         FastAPI         │
                │       (src/api)         │
                └───────────┬─────────────┘
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 ┌────────────┐      ┌──────────────┐     ┌─────────────┐
 │ Retrieval  │      │ Reasoning /  │     │   Metrics   │
 │ (src/retr.)│      │ RAG Pipeline │     │  & Logging  │
 └─────┬──────┘      └───────┬──────┘     └─────┬───────┘
       │                     │                  │
       ▼                     ▼                  │
 ┌─────────────┐       ┌─────────────┐          │
 │ Vector DB   │<----->│  LLM Model  │          │
 │ (FAISS /    │       │ (Embeddings │          │
 │  Weaviate)  │       │  & Inference)          │
 └─────┬───────┘       └─────────────┘          │
       │                                        │
       ▼                                        │
 ┌─────────────┐                                │
 │ Embeddings  │<-------------------------------┘
 │ Generator   │
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │ Ingestion   │  (Kafka Consumer, Data Cleaning)
 │ (src/ingest)│
 └─────┬───────┘
       │
       ▼
 ┌─────────────┐
 │   Data      │  (raw → processed → samples)
 └─────────────┘
```

**Flow Summary**

1. **Data Ingestion** – Streams or batches raw text → cleans & stores.  
2. **Embedding Generation** – Converts text into high-dimensional vectors.  
3. **Indexing** – Stores vectors in FAISS or Weaviate for similarity search.  
4. **Retrieval** – Hybrid dense+sparse retrieval for queries.  
5. **Reasoning / RAG** – Retrieved context fed into LLM for final answer.  
6. **API Layer** – FastAPI serves REST/gRPC endpoints and metrics.

---

##  Repository Structure

```
m2-semantic-engine/
│
├── README.md                  # Project overview, setup, usage
├── LICENSE                    # Choose OS license (MIT/Apache 2.0 etc.)
├── .gitignore
├── pyproject.toml             # Poetry / PDM or setup.cfg + requirements.txt
├── requirements.txt           # (if not using Poetry) Core Python deps
├── requirements-dev.txt       # Testing & linting deps
│
├── docker/
│   ├── Dockerfile             # Main image for API
│   └── worker.Dockerfile      # Optional embedding/worker image
│
├── docs/
│   ├── architecture.md        # High-level architecture diagram + rationale
│   ├── api_reference.md
│   └── design_decisions.md
│
├── data/
│   ├── raw/                   # Unprocessed corpora
│   ├── processed/             # Cleaned/normalized text
│   └── samples/               # Small sample sets for quick tests
│
├── scripts/
│   ├── download_models.py     # Pull pretrained HF or custom models
│   ├── ingest_data.py         # Data ingestion pipeline CLI
│   └── evaluate_embeddings.py # Benchmark embeddings
│
├── configs/
│   ├── default.yaml           # Default configuration
│   ├── production.yaml
│   └── local.yaml
│
├── src/
│   └── semantic_engine/
│       ├── __init__.py
│       ├── settings.py        # Pydantic/Typed settings loader
│       │
│       ├── ingestion/         # Data ingestion & preprocessing
│       │   ├── __init__.py
│       │   └── kafka_consumer.py
│       │
│       ├── embeddings/        # Embedding generation
│       │   ├── __init__.py
│       │   └── generator.py   # Sentence-Transformers / LLaMA embeddings
│       │
│       ├── indexing/          # Vector DB / search layer
│       │   ├── __init__.py
│       │   ├── faiss_indexer.py
│       │   └── weaviate_client.py
│       │
│       ├── retrieval/         # Hybrid dense+sparse retrieval
│       │   ├── __init__.py
│       │   └── retriever.py
│       │
│       ├── reasoning/         # RAG / LLM reasoning
│       │   ├── __init__.py
│       │   └── rag_pipeline.py
│       │
│       ├── api/               # Serving layer
│       │   ├── __init__.py
│       │   ├── main.py        # FastAPI entrypoint
│       │   └── routers/
│       │       └── query.py
│       │
│       └── utils/             # Shared utilities
│           ├── logger.py
│           └── metrics.py
│
├── tests/
│   ├── unit/                  # pytest unit tests
│   ├── integration/
│   └── performance/
│
├── ci/
│   ├── github/
│   │   └── workflows/
│   │       ├── lint-test.yml  # Lint + pytest on push/PR
│   │       └── docker-build.yml
│
└── examples/
    ├── quickstart_notebook.ipynb
    └── api_usage.py
```

---

##  Quick Start

### Install
```bash
git clone https://github.com/<your-username>/M2-Semantic-Engine.git
cd M2-Semantic-Engine
pip install -r requirements.txt
```

### Configure
Edit `configs/local.yaml` to set:
- Model backend (e.g., sentence-transformers/all-mpnet-base-v2)
- Vector DB (FAISS or Weaviate)
- Kafka brokers (for streaming ingestion)

### Run API
```bash
uvicorn src.semantic_engine.api.main:app --reload
```
API will be live at **http://localhost:8000**

---

## Testing
```bash
pytest tests
```

---

## Docker
Build & run the main API image:
```bash
docker build -f docker/Dockerfile -t m2-semantic-engine .
docker run -p 8000:8000 m2-semantic-engine
```

Worker image for embedding jobs:
```bash
docker build -f docker/worker.Dockerfile -t m2-semantic-worker .
```

---

## Documentation
Detailed guides in `docs/`:
- **architecture.md** – UML diagram & rationale  
- **api_reference.md** – REST endpoints  
- **design_decisions.md** – Key technical choices  

Serve docs locally:
```bash
mkdocs serve
```

---

## Contributing
1. Fork & clone  
2. Create a branch: `git checkout -b feature/your-feature`  
3. Commit & push, then open a PR  

Run lint & tests before PR:
```bash
ruff check src tests
pytest
```


---

## Author

**Md Mahbubur Rahman**
[GitHub](https://github.com/m-a-h-b-u-b) | [Website](https://m-a-h-b-u-b.github.io)

---

## Contributing

We welcome contributions!

* Fork the repo and submit pull requests
* Follow Rust coding guidelines and safety best practices
* Report issues or suggest features via GitHub Issues

---
---

## Roadmap
- [ ] Multilingual embeddings  
- [ ] Real-time RAG inference  
- [ ] Kubernetes/Helm deployment  
- [ ] Monitoring dashboard

---

##  Acknowledgments
Powered by **FastAPI**, **Kafka**, **FAISS**, **Weaviate**, and **Hugging Face Transformers**.
