import uuid
import streamlit as st
from llm_helper import LLM


# Estado inicial
if "abot" not in st.session_state:
    st.session_state.abot = LLM()
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("Simpsons Chatbot")

# Inyectar CSS para alinear mensajes y ajustar margen del avatar
st.markdown(
    """
    <style>
    /* Alinea mensajes de usuario a la derecha */
    .stChatMessage:has(.chat-user) {
      display: flex;
      flex-direction: row-reverse;
      text-align: right;
    }
    .stChatMessage:has(.chat-user) [data-testid="stChatMessageContent"] {
      text-align: right;
    }

    /* Reduce espacio arriba del avatar de usuario */
    .stChatMessage:has(.chat-user) img {
      margin-top: 4px;  /* Ajusta este valor según necesites */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(name=message["role"],
                         avatar="icons/bart_192.png" if message["role"]=="user" else "icons/homer_192.png"):
        if message["role"] == "user":
            st.html("<span class='chat-user'></span>")
        st.markdown(message["content"])

# Entrada nueva del usuario
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="icons/bart_192.png"):
        st.html("<span class='chat-user'></span>")
        st.markdown(prompt)

    ai_response = st.session_state.abot.invoke(prompt)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant", avatar="icons/homer_192.png"):
        st.markdown(ai_response)
