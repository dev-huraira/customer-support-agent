from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.knowledge_base import KNOWLEDGE_BASE


def build_documents() -> list[Document]:
    documents = []
    for article in KNOWLEDGE_BASE:
        doc = Document(
            page_content=article["content"],
            metadata={
                "title": article["title"],
                "category": article["category"],
            },
        )
        documents.append(doc)
    return documents


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )
    return splitter.split_documents(documents)


def get_chunked_knowledge_base() -> list[Document]:
    documents = build_documents()
    return chunk_documents(documents)


if __name__ == "__main__":
    chunks = get_chunked_knowledge_base()
    print(f"Produced {len(chunks)} chunks from {len(KNOWLEDGE_BASE)} articles.\n")
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")
        print(f"Title: {chunk.metadata['title']}")
        print(f"Content: {chunk.page_content}\n")