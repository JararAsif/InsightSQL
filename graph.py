from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from state import AgentState
from agents.supervisor import supervisor_agent
from agents.schema_agent import schema_agent
from agents.sql_generator import sql_generator_agent
from agents.validator import sql_validator_agent
from agents.executor import sql_executor_agent
from agents.python_agent import python_agent
from agents.response_agent import response_agent

workflow = StateGraph(AgentState)

workflow.add_node("Supervisor", supervisor_agent)
workflow.add_node("Schema_Agent", schema_agent)
workflow.add_node("SQL_Generator", sql_generator_agent)
workflow.add_node("Validator", sql_validator_agent)
workflow.add_node("Executor", sql_executor_agent)
workflow.add_node("Python_Agent", python_agent)
workflow.add_node("Response_Agent", response_agent)

workflow.add_edge(START, "Supervisor")
workflow.add_edge("Schema_Agent", "SQL_Generator")
workflow.add_edge("SQL_Generator", "Validator")
workflow.add_edge("Executor", "Supervisor")

workflow.add_edge("Python_Agent", "Response_Agent")
workflow.add_edge("Response_Agent", END)

def supervisor_router(state: AgentState):
    return state["next_node"]

workflow.add_conditional_edges(
    "Supervisor",
    supervisor_router,
    {
        "Schema_Agent": "Schema_Agent",
        "Python_Agent": "Python_Agent",
        "Response_Agent": "Response_Agent",
        "FINISH": END
    }
)

def validator_router(state: AgentState):
    if len(state.get("sql_errors", [])) > 0:
        print("    -> Validator failed, looping back to SQL Generator...")
        return "retry"
    else:
        print("    -> Validator passed, proceeding to Executor.")
        return "valid"

workflow.add_conditional_edges(
    "Validator",
    validator_router,
    {
        "retry": "SQL_Generator",
        "valid": "Executor"
    }
)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

if __name__ == '__main__':
    from langchain_core.messages import HumanMessage

    config = {"configurable": {"thread_id": "test_thread_1"}}
    
    print("\n--- Starting Test ---")
    user_input = "What is the name of the project with the largest budget?"
    print(f"User: {user_input}")

    result = app.invoke(
        {"messages": [HumanMessage(content=user_input)]}, 
        config=config
    )
    
    print("\n--- Final Response ---")
    print(result["messages"][-1].content)
