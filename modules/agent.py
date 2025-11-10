import os
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from modules.tools import tools
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

load_dotenv()

def initialize_agent():
    groq_api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        st.warning("Please enter your Groq API key in the sidebar to start using the assistant.")
        return None

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=None,
        api_key=groq_api_key
    )
    max_iterations = 2
    agent_executor = create_react_agent(
        model=llm,
        tools=tools,
        debug=True
    )
    agent_executor = agent_executor.with_config(
        recursion_limit=2 * max_iterations + 1
    )
    return agent_executor, llm
