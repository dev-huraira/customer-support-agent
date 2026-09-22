import os
from langchain_postgres import PGVectorStore, PGEngine
from rag.embeddings import embeddings

VECTOR_DB_URI = os.getenv("VECTOR_DB_URL")
TABLE_NAME = "knowledge_base_vectors"

pg_engine = PGEngine.from_connection_string(url=VECTOR_DB_URI)

vector_store = PGVectorStore.create_sync(
    engine=pg_engine,
    table_name=TABLE_NAME,
    embedding_service=embeddings,
)