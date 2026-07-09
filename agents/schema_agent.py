from state import AgentState
from tools.sql_tools import get_schema

def schema_agent(state: AgentState) -> dict:
    """
    Node: Schema Agent
    Responsibility: Retrieve the database schema and add it to the state.
    
    Notice this agent does NOT use an LLM. It is simply a programmatic 
    function that fetches data to enrich the state for the next LLM agent.
    """
    print("--- [Agent] Schema Agent running ---")
    
    schema_info = get_schema()
    
    return {"schema": schema_info}
