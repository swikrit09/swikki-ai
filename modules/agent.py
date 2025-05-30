import os
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from modules.tools import tools
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

load_dotenv()

# Read API key from environment or Streamlit session
groq_api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")

# Only initialize agent if API key is present
if groq_api_key:
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=None,
        api_key=groq_api_key
    )

    agent_executor = create_react_agent(
        model=llm,
        tools=tools,
        debug=True
        # checkpointer = InMemorySaver()  # Optional
    )
else:
    st.warning("Please enter your Groq API key in the sidebar to start using the assistant.")
    agent_executor = None
