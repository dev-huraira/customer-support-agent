import uuid
from graph import graph
from utils import extract_text


def run_message(text: str, thread_id: str = None) -> dict:
    thread_id = thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    return graph.invoke(
        {"messages": [{"role": "user", "content": text}], "user_id": "user_101"},
        config=config,
    )


def test_billing_routing():
    result = run_message("I want a refund for invoice INV-002")
    assert result["category"] == "billing"


def test_technical_routing():
    result = run_message("the app keeps crashing when I open it")
    assert result["category"] == "technical"


def test_general_routing():
    result = run_message("hi, how are you?")
    assert result["category"] == "general"


def test_billing_tool_invocation():
    result = run_message("check my invoices for user_101")
    reply = extract_text(result["messages"][-1].content)
    assert "INV" in reply or "invoice" in reply.lower()


def test_technical_rag_paraphrase():
    result = run_message("why is my app so laggy")
    reply = extract_text(result["messages"][-1].content)
    assert "slow" in reply.lower() or "loading" in reply.lower()


def test_context_persists_across_turns():
    thread_id = str(uuid.uuid4())
    run_message("my user id is user_101", thread_id=thread_id)
    result = run_message("check my invoices", thread_id=thread_id)
    assert result["category"] == "billing"