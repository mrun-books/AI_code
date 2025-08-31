
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.schema import AgentAction, AgentFinish
from dotenv import load_dotenv

# --- Import your tools ---
from tools import DdgSearchTool, GoogleSearchTool, TavilySearchTool, AcademicSearchTool, ss_SearchTool

load_dotenv()

# Custom output parser that's more forgiving
class ForgivingReActOutputParser(ReActSingleInputOutputParser):
    def parse(self, llm_output: str) -> AgentAction | AgentFinish:
        # Handle case where LLM provides direct answer without proper format
        if "Final Answer:" in llm_output:
            parts = llm_output.split("Final Answer:")
            if len(parts) > 1:
                return AgentFinish({"output": parts[-1].strip()}, llm_output)
        
        # If no "Thought:" at start, add it
        if not llm_output.strip().startswith("Thought:"):
            # Check if this looks like a direct answer
            if not any(keyword in llm_output.lower() for keyword in ["action:", "search", "query"]):
                return AgentFinish({"output": llm_output.strip()}, llm_output)
            else:
                llm_output = "Thought: " + llm_output
        
        # Try the parent parser
        try:
            return super().parse(llm_output)
        except Exception as e:
            # If parsing fails, treat as final answer
            return AgentFinish({"output": llm_output.strip()}, llm_output)

# Start with fewer, more reliable tools
tools_list = [DdgSearchTool, GoogleSearchTool]

# Chat prompt with required ReAct variables
Research_agent_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant. For simple questions, answer directly. For information you don't know, use search tools.

You have access to these tools: {tools}

Use this format:
Thought: [think about what to do]
Action: [tool name - must be one of: {tool_names}]
Action Input: [search query if using tool]
Observation: [tool result]
Thought: I now know the final answer
Final Answer: [your final answer]

For simple greetings, math, or general knowledge, go straight to Final Answer.

Examples:
Simple: Thought: This is a greeting\nFinal Answer: Hello! How can I help?
Search: Thought: I need current info\nAction: DDG Search tool\nAction Input: latest AI news"""),
    (MessagesPlaceholder(variable_name="chat_history")),
    ("human", "{input}"),
    ("assistant", "{agent_scratchpad}"),
])

# ✅ Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize agent once globally
search_agent = None

# Function to initialize agent (with memory)
def initialize_research_agent() -> AgentExecutor:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    dr_agent = create_react_agent(
        tools=tools_list,
        llm=llm,
        prompt=Research_agent_prompt,
        output_parser=ForgivingReActOutputParser()
    )

    # Pass memory into AgentExecutor with more iterations for search queries
    return AgentExecutor(
        agent=dr_agent, 
        tools=tools_list, 
        memory=memory, 
        handle_parsing_errors=True,
        verbose=False,
        max_iterations=4,
        max_execution_time=60,
        return_intermediate_steps=False
    )


# Function to run agent with chat history
def get_agent_response(message: str) -> dict:
    global search_agent
    
    # Initialize agent only once
    if search_agent is None:
        search_agent = initialize_research_agent()
    
    response = search_agent.invoke({"input": message})
    
    # Get chat history from memory
    chat_history = memory.load_memory_variables({})["chat_history"]
    
    # Convert to expected format for FastAPI
    messages = []
    for msg in chat_history:
        if hasattr(msg, 'type'):
            messages.append(msg)
        else:
            # Handle string messages
            messages.append(type('Message', (), {'type': 'ai', 'content': str(msg)})())
    
    return {"messages": messages, "output": response["output"]}


# --- Example usage ---
if __name__ == "__main__":
    print(get_agent_response("Hello agent!"))
    print(get_agent_response("Can you summarize recent papers on transformers?"))
    print(get_agent_response("What did I ask first?"))

    # Inspect memory
    print("\n--- Conversation History ---")
    print(memory.load_memory_variables({})["chat_history"])
