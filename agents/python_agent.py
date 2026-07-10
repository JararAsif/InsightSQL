import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from state import AgentState
from tools.python_tool import execute_python

def python_agent(state: AgentState) -> dict:
    """
    Node: Python Agent
    Responsibility: Generate python code to draw a chart using matplotlib, and execute it.
    """
    print("--- [Agent] Python Agent running ---")
    llm = ChatOllama(model="qwen3.5:2b", temperature=0.0, reasoning=False)
    
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'python.txt')
    with open(prompt_path, 'r') as f:
        system_prompt = f.read()
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({
        "raw_results": state.get("raw_results", ""),
        "messages": state["messages"]
    })
    
    code = response.content.strip()

    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
        
    execution_output = execute_python(code)
    print(f"Python Output: {execution_output}")
    
    if "Error" in str(execution_output) or "Traceback" in str(execution_output):
        return {"visualization_path": None}
    else:
        return {"visualization_path": "chart.png"}
