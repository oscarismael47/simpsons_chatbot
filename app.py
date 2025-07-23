import uuid
import streamlit as st
from llm_helper import LLM


st.title("Homer Chatbot")


# Initialize session state
if "abot" not in st.session_state:
    st.session_state.abot = LLM()

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(name=message["role"], avatar="icons/bart.png" if message["role"] == "user" else "icons/homer.png"):
        st.markdown(message["content"])

# Handle new user input
if message := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user", avatar="icons/bart.png"):
        st.markdown(message)

    ai_response = st.session_state.abot.invoke(message)
    with st.chat_message("assistant", avatar="icons/homer.png"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})