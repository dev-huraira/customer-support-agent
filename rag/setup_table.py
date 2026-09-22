from dotenv import load_dotenv
load_dotenv()

import os
from langchain_postgres import PGEngine

VECTOR_DB_URI = os.getenv("VECTOR_DB_URL")
TABLE_NAME = "knowledge_base_vectors"

pg_engine = PGEngine.from_connection_string(url=VECTOR_DB_URI)

pg_engine.init_vectorstore_table(
    table_name=TABLE_NAME,
    vector_size=3072,
    overwrite_existing=True,
)

print(f"Table '{TABLE_NAME}' is ready.")