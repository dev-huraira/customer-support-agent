from langchain_core.tools import tool
from rag.vector_store import vector_store

MOCK_SYSTEM_STATUS = {
    "user_101": {"account_status": "active", "last_login": "2026-09-18", "known_issues": []}
}


@tool
def search_docs(query: str) -> str:
    """Search the technical knowledge base for articles relevant to the query.
    Returns the most relevant passages along with their source article titles."""
    results = vector_store.similarity_search_with_score(query, k=3)

    if not results:
        return "No relevant articles found in the knowledge base."

    formatted = []
    for doc, score in results:
        title = doc.metadata.get("title", "Untitled")
        formatted.append(f"[Source: {title}]\n{doc.page_content}")

    return "\n\n".join(formatted)


@tool
def run_diagnostic(user_id: str) -> str:
    """Run a diagnostic check on a user's account to identify known issues or system status."""
    status = MOCK_SYSTEM_STATUS.get(user_id)
    if not status:
        return f"No system status found for user {user_id}."

    if not status["known_issues"]:
        return f"Account {user_id} is {status['account_status']}. Last login: {status['last_login']}. No known issues detected."

    issues = ", ".join(status["known_issues"])
    return f"Account {user_id} is {status['account_status']}. Known issues: {issues}."