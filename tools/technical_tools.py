from langchain_core.tools import tool

KNOWLEDGE_BASE = [
    {
        "title": "Resetting your password",
        "content": "Go to Settings > Security > Reset Password. A reset link is sent to your registered email and expires in 15 minutes."
    },
    {
        "title": "App crashes on startup",
        "content": "Clear the app cache from Settings > Storage. If the crash persists, uninstall and reinstall the latest version."
    },
    {
        "title": "Two-factor authentication setup",
        "content": "Enable 2FA under Settings > Security > Two-Factor Auth. You can use an authenticator app or SMS codes."
    },
    {
        "title": "Slow loading times",
        "content": "Slow loading is usually caused by a weak network connection or an outdated app version. Update the app and check your connection speed."
    },
]


MOCK_SYSTEM_STATUS = {
    "user_101": {"account_status": "active", "last_login": "2026-09-18", "known_issues": []}
}


@tool
def search_docs(query:str) -> str:
    """Search the technical knowledge base for the article related to query. Return matching articles and content"""
    query_words=set(query.lower().split())
    matches=[]


    for article in KNOWLEDGE_BASE:
        article_words=set((article['title']+ " " + article["content"]).lower().split())
        if query_words & article_words:
            matches.append(f"{article['title']}: {article['content']}")

    if not matches:
        return "No relevant articles found in the knowledge base."

    return "\n\n".join(matches)

@tool
def run_diagnostic(user_id:str) -> str:
    """Run a diagnostic on the user account to identify known issues and system status"""
    status = MOCK_SYSTEM_STATUS.get(user_id)
    if not status:
        return f"No system status found for user {user_id}."

    if not status["known_issues"]:
        return f"Account {user_id} is {status['account_status']}. Last login: {status['last_login']}. No known issues detected."

    issues = ", ".join(status["known_issues"])
    return f"Account {user_id} is {status['account_status']}. Known issues: {issues}."
