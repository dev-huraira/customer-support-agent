from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

general_agent = create_agent(
    llm,
    tools=[],
    system_prompt=(
        "You are a friendly general support agent. Answer FAQs and general "
        "questions politely. If the question is about billing or a technical "
        "issue, say you'll connect them with the right specialist."
    ),
)