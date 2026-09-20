from dotenv import load_dotenv
load_dotenv()

import os
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from state import AgentState
from supervisor import supervisor_node
from agents.billing_agent import billing_agent
from agents.technical_agent import technical_agent
from agents.general_agent import general_agent
from logging_config import setup_logging, logger

setup_logging()

FALLBACK_MESSAGE = {
    "role": "assistant",
    "content": "Sorry, something went wrong on our end handling that. Could you try rephrasing, or ask again in a moment?",
}


def _run_agent_safely(agent, agent_name: str, state: AgentState) -> dict:
    try:
        result = agent.invoke({"messages": state["messages"]})
        new_messages = result["messages"][len(state["messages"]):]
        return {"messages": new_messages}
    except Exception as e:
        logger.error(f"{agent_name} agent failed: {e}")
        return {"messages": [FALLBACK_MESSAGE]}


def billing_node(state: AgentState) -> dict:
    return _run_agent_safely(billing_agent, "billing", state)


def technical_node(state: AgentState) -> dict:
    return _run_agent_safely(technical_agent, "technical", state)


def general_node(state: AgentState) -> dict:
    return _run_agent_safely(general_agent, "general", state)


graph_builder = StateGraph(AgentState)

graph_builder.add_node("supervisor", supervisor_node)
graph_builder.add_node("billing", billing_node)
graph_builder.add_node("technical", technical_node)
graph_builder.add_node("general", general_node)

graph_builder.add_edge(START, "supervisor")
graph_builder.add_edge("billing", END)
graph_builder.add_edge("technical", END)
graph_builder.add_edge("general", END)

DB_URI = os.getenv("DATABASE_URL")

pool = ConnectionPool(
    conninfo=DB_URI,
    max_size=20,
    kwargs={"autocommit": True, "row_factory": dict_row},
)

checkpointer = PostgresSaver(pool)
checkpointer.setup()

graph = graph_builder.compile(checkpointer=checkpointer)