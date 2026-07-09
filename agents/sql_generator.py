import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from state import AgentState

def sql_generator_agent(state: AgentState) -> dict:
    """
    Node: SQL Generator Agent
    Responsibility: Translate the user's natural language into a raw SQLite query.
    """
    print("--- [Agent] SQL Generator Agent running ---")
    
    llm = ChatOllama(model="qwen3.5:2b", temperature=0.0, reasoning=False)
    
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'sql.txt')
    with open(prompt_path, 'r') as f:
        system_prompt = f.read()
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    schema = state.get("schema", "No schema available.")
    errors = state.get("sql_errors", [])
    errors_str = "\n".join(errors) if errors else "None"
    
    chain = prompt | llm
    
    response = chain.invoke({
        "schema": schema,
        "sql_errors": errors_str,
        "messages": state["messages"]
    })
    
    print(f"Generated SQL: {response.content}")
    return {"sql_query": response.content.strip()}
