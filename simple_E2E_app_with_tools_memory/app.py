from fastapi import FastAPI
from pydantic import BaseModel
from agent_with_chat_history import get_agent_response
from langchain_core.runnables import RunnableConfig

app = FastAPI()


class Query(BaseModel):
    question: str


@app.post("/ask")
async def ask_agent(query: Query):
    thread_id = "thread_1"

    # Create a RunnableConfig with the thread_id
    # The thread_id is placed within the 'configurable' key of the config dictionary
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    # Run agent
    result = get_agent_response(query.question)
    print(type(result))

    # Log conversation in uvicorn server
    print("\n--- Conversation ---")
    history = []
    for msg in result["messages"]:
        role = getattr(msg, "type", "unknown")  # "human" / "ai"
        print(f"{role.upper()}: {msg.content}")
        history.append({"role": role, "content": msg.content, "thread_id": thread_id})
    print("-------------------\n")

    # Return full conversation to frontend
    return {"history": history}
