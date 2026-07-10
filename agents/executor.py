from state import AgentState
from tools.sql_tools import execute_query

def sql_executor_agent(state: AgentState) -> dict:
    print("--- [Agent] SQL Executor Agent running ---")

    query = state.get("sql_query")
    raw_results = execute_query(query)
    
    return {"raw_results": str(raw_results)}
