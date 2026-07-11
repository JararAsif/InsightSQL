import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from langchain_core.messages import HumanMessage, AIMessage
from graph import app as langgraph_app
st.set_page_config(page_title="Multi-Agent SQL Assistant", layout="wide", page_icon="🤖")

st.title("LangGraph Multi-Agent SQL Assistant")
st.markdown("Ask questions about the company database, or ask to plot charts!")


if "thread_id" not in st.session_state:
    st.session_state.thread_id = "session_1"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "sql_query" not in st.session_state:
    st.session_state.sql_query = ""
if "raw_results" not in st.session_state:
    st.session_state.raw_results = ""
if "agent_steps" not in st.session_state:
    st.session_state.agent_steps = []

with st.sidebar:
    st.header("Diagnostics & Logs")
    
    st.subheader("Execution Trace")
    for step in st.session_state.agent_steps:
        st.text(f"→ {step}")
        
    st.subheader("Generated SQL")
    if st.session_state.sql_query:
        st.code(st.session_state.sql_query, language="sql")
        
    st.subheader("Raw SQLite Data")
    if st.session_state.raw_results:
        st.text_area("Results", st.session_state.raw_results, height=150)

for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

if user_input := st.chat_input("Ask a question about the database... (e.g. 'Show average salary by department')"):
    
    user_msg = HumanMessage(content=user_input)
    st.session_state.chat_history.append(user_msg)
    with st.chat_message("user"):
        st.markdown(user_input)
        
    st.session_state.agent_steps = []
    st.session_state.sql_query = ""
    st.session_state.raw_results = ""
    
    with st.chat_message("assistant"):
        status_text = st.empty()
        status_text.markdown("💭 Agents are thinking...")
        
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        chart_generated = None
        
        for event in langgraph_app.stream({"messages": [user_msg]}, config=config):
            for node_name, state_update in event.items():
                st.session_state.agent_steps.append(f"Node Executed: {node_name}")
                
                if "sql_query" in state_update:
                    st.session_state.sql_query = state_update["sql_query"]
                if "raw_results" in state_update:
                    st.session_state.raw_results = state_update["raw_results"]
                
                if "visualization_path" in state_update and state_update["visualization_path"]:
                    chart_generated = state_update["visualization_path"]
        
        full_state = langgraph_app.get_state(config).values
        if "messages" in full_state and len(full_state["messages"]) > 0:
            final_msg = full_state["messages"][-1]
            if isinstance(final_msg, AIMessage):
                status_text.markdown(final_msg.content)
                st.session_state.chat_history.append(final_msg)
            else:
                status_text.empty()
        else:
            status_text.empty()
        if chart_generated and os.path.exists(chart_generated):
            st.image(chart_generated)
            try:
                os.remove(chart_generated)
            except Exception:
                pass
