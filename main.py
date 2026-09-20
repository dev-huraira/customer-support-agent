from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import extract_text

from graph import graph
from logging_config import logger

app = FastAPI(title="Customer Support Multi-Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    user_id: str
    thread_id: str


class ChatResponse(BaseModel):
    reply: str
    category: str
    thread_id: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}

    try:
        result = graph.invoke(
            {
                "messages": [{"role": "user", "content": request.message}],
                "user_id": request.user_id,
            },
            config=config,
        )

        last_message = result["messages"][-1]

        return ChatResponse(
            reply=extract_text(last_message.content),
            category=result.get("category", "unknown"),
            thread_id=request.thread_id,
        )

    except Exception as e:
        logger.error(f"Chat request failed for thread {request.thread_id}: {e}")
        return ChatResponse(
            reply="Sorry, something went wrong processing your message. Please try again.",
            category="error",
            thread_id=request.thread_id,
        )