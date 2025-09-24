# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine


from pathlib import Path
from typing import List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # Project paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    CONFIG_DIR: Path = BASE_DIR / "configs"

    # Vector DB settings
    VECTOR_DB_TYPE: str = Field("faiss", description="Type of vector database: faiss or weaviate")
    VECTOR_DB_PATH: Optional[Path] = Field(DATA_DIR / "faiss_index", description="Path for FAISS index storage")
    WEAVIATE_URL: Optional[str] = None

    # Model / Embeddings settings
    MODEL_NAME: str = Field("sentence-transformers/all-mpnet-base-v2", description="Hugging Face model name")
    EMBEDDING_DIM: int = 768

    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True

    # Kafka / Streaming settings
    KAFKA_BROKER_URL: Optional[str] = "localhost:9092"
    KAFKA_TOPIC: Optional[str] = "semantic_engine"

    # Misc
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
