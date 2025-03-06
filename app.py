import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

st.set_page_config(page_title="AT0M ", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    body {background-color: #0F172A !important;}
    .stChatContainer {display: flex; flex-direction: column-reverse;}
    .stChatMessage {border-radius: 10px; padding: 10px; margin: 5px 0;}
    .stChatMessageUser {background-color: #1E293B; color: #E2E8F0;}
    .stChatMessageBot {background-color: #334155; color: #F1F5F9;}
    .stChatBox {background-color: #1E293B; color: white; border-radius: 10px; padding: 10px;}
    .stButton button {background-color: #DC2626 !important; color: white !important; border-radius: 10px !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #E2E8F0;'>🔥 AT0M </h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are AT0M, a dumb and angry Girl who gives answers in a unique way, never agrees with anyone, and messes with people."}]

if "last_input" not in st.session_state:
    st.session_state.last_input = None

chat_container = st.container()
for msg in st.session_state.messages[1:]:
    role_class = "stChatMessageUser" if msg["role"] == "user" else "stChatMessageBot"
    chat_container.markdown(f"<div class='stChatMessage {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

user_input = st.text_input("Type your message...", key="user_input", placeholder="Good luck ", label_visibility="collapsed")

if user_input and user_input != st.session_state.last_input:
    st.session_state.last_input = user_input
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=st.session_state.messages[-6:],  
        temperature=1.5,
        max_tokens=200,
        top_p=1,
        stream=True
    )

    bot_reply = ""
    bot_placeholder = chat_container.empty()

    for chunk in response:
        word = chunk.choices[0].delta.content or ""
        bot_reply += word
        bot_placeholder.markdown(f"<div class='stChatMessage stChatMessageBot'>{bot_reply}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()
