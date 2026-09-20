from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.technical_tools import search_docs,run_diagnostic

llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

technical_agent=create_agent(
    llm,
    tools=[search_docs,run_diagnostic],
    system_prompt=("""You are technical support agent diagnose the issue and search the knowledge base 
    to help user resolve problem.Be specific and reference articles title when you use them"""),
)