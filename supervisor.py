from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
from state import AgentState
from logging_config import logger

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")


class RouteDecision(BaseModel):
    next: Literal["billing", "technical", "general"] = Field(
        description="Which specialist agent should handle this query"
    )


def supervisor_node(state: AgentState) -> Command[Literal["billing", "technical", "general"]]:
    messages = state["messages"]

    routing_prompt = SystemMessage(content=(
        "You are a supervisor managing three specialist agents: billing, technical, and general.\n"
        "Based on the full conversation, decide which specialist should handle the latest user message.\n"
        "- billing: invoices, refunds, payments, charges, payment methods\n"
        "- technical: bugs, errors, login issues, crashes, how-to questions\n"
        "- general: greetings, small talk, unclear or unrelated requests"
    ))

    structured_llm = llm.with_structured_output(RouteDecision)

    try:
        decision = structured_llm.invoke([routing_prompt] + messages)
        route = decision.next
        logger.info(f"Routing decision: {route} | last message: {messages[-1].content[:80]!r}")
    except Exception as e:
        logger.error(f"Supervisor routing failed, defaulting to general. Error: {e}")
        route = "general"

    return Command(
        goto=route,
        update={"category": route, "next": route},
    )