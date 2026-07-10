import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama
from state import AgentState

def response_agent(state: AgentState) -> dict:
    """
    Node: Response Agent
    Responsibility: Create a natural language answer based on the SQL results or chat history.
    """
    print("--- [Agent] Response Agent running ---")
    llm = ChatOllama(model="qwen3.5:2b", temperature=0.0, reasoning=False)
    
    if not state.get("sql_query"):
        system_prompt = (
            "You are a helpful database assistant.\n"
            "The user is saying hello, chatting, or asking a general question not related to querying the database.\n"
            "Respond to them in a friendly, professional, and helpful manner.\n\n"
            "CRITICAL INSTRUCTION: Do NOT output any <think> tags, thought processes, or reasoning. Output ONLY the final response directly."
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        chain = prompt | llm
        response = chain.invoke({
            "messages": state["messages"]
        })
    else:
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'response.txt')
        with open(prompt_path, 'r') as f:
            system_prompt = f.read()
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages")
        ])
        chain = prompt | llm
        response = chain.invoke({
            "raw_results": state.get("raw_results", ""),
            "sql_query": state.get("sql_query", ""),
            "visualization_path": state.get("visualization_path", ""),
            "messages": state["messages"]
        })
    
    return {
        "messages": [AIMessage(content=response.content)],
        "sql_query": "",
        "raw_results": "",
        "visualization_path": None,
        "schema": "",
        "sql_errors": []
    }
