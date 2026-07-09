import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from state import AgentState

def supervisor_agent(state: AgentState) -> dict:
    """
    Node: Supervisor Agent
    Responsibility: Act as the brain of the graph. Read the conversation 
    and decide which agent runs next.
    """
    print("--- [Agent] Supervisor Agent running ---")

    llm = ChatOllama(model="qwen3.5:2b", temperature=0.0, reasoning=False)
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'supervisor.txt')
    with open(prompt_path, 'r') as f:
        system_prompt = f.read()
    
    has_results = "YES" if state.get("raw_results") else "NO"
    system_prompt += f"\n\nSystem Note: Has the database query been executed yet? {has_results}"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    chain = prompt | llm

    response = chain.invoke({
        "messages": [state["messages"][-1]]
    })
    
    next_node = response.content.strip()
    
    valid_nodes = ["Schema_Agent", "Python_Agent", "Response_Agent", "FINISH"]
    
    final_next = "FINISH" 
    for node in valid_nodes:
        if node in next_node:
            final_next = node
            break
            
    if state.get("raw_results") and final_next == "Schema_Agent":
        user_msg = state["messages"][-1].content.lower()
        if any(word in user_msg for word in ["chart", "graph", "plot"]):
            print("    -> [Safety Override] Query executed, user wants chart. Forcing route to Python_Agent.")
            final_next = "Python_Agent"
        else:
            print("    -> [Safety Override] Query already executed. Forcing route to Response_Agent.")
            final_next = "Response_Agent"
            
    if not state.get("raw_results") and final_next == "Python_Agent":
        print("    -> [Safety Override] User wants a chart, but we have no data yet. Forcing route to Schema_Agent.")
        final_next = "Schema_Agent"
            
    print(f"    -> Routing to: {final_next}")
    
    return {"next_node": final_next}
