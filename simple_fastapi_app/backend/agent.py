from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END
#from  app.config import OPENAI_API_KEY
from dotenv import load_dotenv
import os

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Create an LLM (OpenAI GPT model)
llm = ChatOpenAI( model="gpt-4o-mini",api_key=OPENAI_API_KEY)

print("API Key Loaded?", os.getenv("OPENAI_API_KEY") is not None)

# Define how the agent responds
def call_llm(state: MessagesState):
    response = llm.invoke(state["messages"])  
    # Append LLM response to existing messages
    return {"messages": state["messages"] + [response]}

# Build a graph with one node (the LLM)
graph = StateGraph(MessagesState)
graph.add_node("llm", call_llm)   # add LLM as a node
graph.set_entry_point("llm")      # start here
graph.add_edge("llm", END)        # end after LLM finishes

# Compile the graph into an executable agent
agent = graph.compile()
