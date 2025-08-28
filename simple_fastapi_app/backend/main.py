from fastapi import FastAPI
from pydantic import BaseModel
from backend.agent import agent

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_agent(query: Query):
    # Run agent
    result = agent.invoke({"messages": [("user", query.question)]})

    # Log conversation in uvicorn server
    print("\n--- Conversation ---")
    history = []
    for msg in result["messages"]:
        role = getattr(msg, "type", "unknown")  # "human" / "ai"
        print(f"{role.upper()}: {msg.content}")
        history.append({"role": role, "content": msg.content})
    print("-------------------\n")

    # Return full conversation to frontend
    return {"history": history}
