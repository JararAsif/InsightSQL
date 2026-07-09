import os
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from state import AgentState

def sql_validator_agent(state: AgentState) -> dict:
    """
    Node: SQL Validator Agent
    Responsibility: Check the generated SQL for safety and correctness.
    If errors are found, they are appended to the state so the generator can retry.
    """
    print("--- [Agent] SQL Validator Agent running ---")
    query = state.get("sql_query", "")
    schema = state.get("schema", "")
    
    errors = state.get("sql_errors", [])
    
    dangerous_keywords = ["DROP ", "DELETE ", "UPDATE ", "INSERT ", "ALTER "]
    upper_query = query.upper()
    for keyword in dangerous_keywords:
        if keyword in upper_query:
            errors.append(f"Security Error: Query contains forbidden keyword '{keyword}'. Only SELECT is allowed.")
            return {"sql_errors": errors}
            
    llm = ChatOllama(model="qwen3.5:2b", temperature=0.0, reasoning=False)
    
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'validator.txt')
    with open(prompt_path, 'r') as f:
        prompt_text = f.read()
        
    prompt = PromptTemplate.from_template(prompt_text)
    chain = prompt | llm
    
    response = chain.invoke({"sql_query": query, "schema": schema})
    validation_result = response.content.strip()
    print("validation_result", validation_result)
    
    if validation_result.startswith("VALID"):
        return {"sql_errors": []}
    else:
        errors.append(f"Validation Error: {validation_result}")
        return {"sql_errors": errors}
