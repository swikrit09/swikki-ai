import asyncio
import streamlit as st
from modules.voice import listen
from modules.agent import initialize_agent
from langchain.schema import HumanMessage, AIMessage
from modules.tools import tools

st.set_page_config(
    page_title="Swikki AI - Your Voice Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title("Swikki AI - Your Voice Assistant")
with st.sidebar:
    st.header("About")
    st.markdown("""
    Swikki Ai is a voice assistant that can help you with various tasks. 
    You can type or speak your commands, and it will respond accordingly.
    """)

    st.header("How to Use")
    st.markdown("""
    1. Add your Groq API key in the input box below.
    2. Click the "Speak" button to use voice input or type your command in the input box.
    3. Click the "Send" button to get a response from the assistant.
    4. You can also view the response metadata and tool calls if available.
    """)
    st.text_input("Groq API Key", type="password", key="groq_api_key")
    
    st.header("Available Tools")
    for tool in tools:
        name = getattr(tool, "name", "Unknown")
        st.markdown(f"- {name}")
    

# Function to show response
def show_response(response):
    for msg in response["messages"]:
        # Distinguish message type
        content = getattr(msg, "content", "")
        if isinstance(msg, HumanMessage):
            st.markdown(f"> **🧑 You:**  {content}")
        elif isinstance(msg, AIMessage):
            if(content not in ["","null"]):
                st.markdown(f"> **🤖 Assistant:**  {content}")
        else:
            if content and content.strip().lower() != "null":
                st.markdown(f"> {content}")

        # Tool Calls (if any)
        additional_kwargs = getattr(msg, "additional_kwargs", {})
        tool_calls = additional_kwargs.get("tool_calls", [])
        if tool_calls:
            for tool_call in tool_calls:
                function = tool_call.get("function", {})
                tool_name = function.get("name", "Unknown")
                arguments = function.get("arguments", "{}")
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"**🔧 Tool Name:** ")
                    st.code(f'def {tool_name}()', language="python")
                with c2:
                    st.markdown("**📦 Arguments:**")
                    st.code(arguments, language="json")

        # Metadata (if available)
        metadata = getattr(msg, "response_metadata", {})
        if metadata:
            with st.expander("📊 Response Metadata", expanded=False):
                token_usage = metadata.get("token_usage", {})
                model_name = metadata.get("model_name", "N/A")

                st.markdown("#### 🔢 Token Usage")
                st.write({
                    "Input Tokens": token_usage.get("prompt_tokens", "N/A"),
                    "Output Tokens": token_usage.get("completion_tokens", "N/A"),
                    "Total Tokens": token_usage.get("total_tokens", "N/A")
                })

                st.markdown("#### ⏱ Timing Info (sec)")
                st.write({
                    "Completion Time": round(token_usage.get("completion_time", 0), 3),
                    "Prompt Time": round(token_usage.get("prompt_time", 0), 3),
                    "Queue Time": round(token_usage.get("queue_time", 0), 3),
                    "Total Time": round(token_usage.get("total_time", 0), 3)
                })

                st.markdown(f"#### 🤖 Model Used: `{model_name}`")

# Function to show a listening GIF
def show_gif():
    left_co, cent_co, last_co = st.columns([1,10,1])
    with cent_co:
        if st.session_state.get('listening', False):
            st.markdown(
                """
                <img src="https://media0.giphy.com/media/J0Hok3il7qxAEegXj9/giphy.gif" width="500px" style="border-radius: 10px;">
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <img src="https://media2.giphy.com/media/c7Na3gbE3MyFW65bxz/200w.gif" width="300px" style="border-radius: 10px;">
                """,
                unsafe_allow_html=True
            )

def run_async_task(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

# Session defaults
if "response" not in st.session_state:
    st.session_state["response"] = {"messages": []}
if "default_text" not in st.session_state:
    st.session_state["default_text"] = ""
if "listening" not in st.session_state:
    st.session_state["listening"] = False
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Buttons
with st.container():
    col1,col2= st.columns(2)
    with col1:
        if st.button("Speak"):
            st.session_state["listening"] = True
            show_gif()
            text = listen()
            if not text.startswith("Error:"):
                st.session_state["default_text"] = text
            st.session_state["listening"] = False
            st.rerun()
    if st.session_state.get("listening", False):
        print("Not Listening")
        show_gif()

col1,col2 = st.columns([4,1], gap="small", vertical_alignment="bottom")

with col1:
    command_input = st.text_input("Type or edit your command:", value=st.session_state.get("default_text", ""), key="command_input")
with col2:
    if st.button("Send"):
        if command_input.strip():
            agent_executor,llm = initialize_agent()
            response = {}
            st.session_state["chat_history"].append({"role": "user", "content": command_input})
            try: 
                response = agent_executor.invoke({"messages": [{"role": "user", "content": command_input}]})
            except Exception as e:
                ans = llm.invoke('You are a helpful assistant. Please provide a answer for the query: ' + command_input)
                response = {
                    "messages": [
                        AIMessage(
                            content=ans.content.strip(),
                            response_metadata={
                                "model_name": llm.model_name
                            }
                        )
                    ]
                }
                # speak(ans.content.strip())
            st.session_state["response"] = response
            st.session_state["chat_history"].append({"role": "assistant", "content": response["messages"][-1].content})
            st.session_state["default_text"] = ""  # Clear after sending
            # st.rerun()

with st.expander("Chat History", expanded=False):
    if st.session_state["chat_history"]:
        for msg in st.session_state["chat_history"]:
            role = msg["role"].capitalize()
            content = msg["content"]
            st.markdown(f"**{role}:** {content}")
    else:
        st.markdown("No chat history yet.")
# Show output
show_response(st.session_state["response"])
