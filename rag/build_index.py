from dotenv import load_dotenv
load_dotenv()

from rag.ingest import get_chunked_knowledge_base
from rag.vector_store import vector_store


def main():
    chunks = get_chunked_knowledge_base()
    print(f"Embedding and storing {len(chunks)} chunks...")

    vector_store.add_documents(chunks)

    print("Done. Knowledge base is now searchable.")


if __name__ == "__main__":
    main()