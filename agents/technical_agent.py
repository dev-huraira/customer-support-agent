from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.technical_tools import search_docs, run_diagnostic

llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

technical_agent = create_agent(
    llm,
    tools=[search_docs, run_diagnostic],
    system_prompt=(
        "You are a technical support agent. Diagnose issues and search the "
        "knowledge base to help users resolve problems. "
        "The search tool returns passages tagged with [Source: <title>] — "
        "always mention which article your answer is based on. "
        "If the retrieved passages don't actually address the user's question, "
        "say so honestly rather than guessing."
    ),
)