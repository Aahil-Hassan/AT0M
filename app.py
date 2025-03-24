import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ChatGPT-like UI Design
st.set_page_config(page_title="AT0M Chat", page_icon="💬", layout="wide")

st.markdown(
    """
    <style>
    body {background-color: #F7F7F8 !important;}
    .stChatContainer {padding: 10px; border-radius: 8px;}
    .stChatMessage {border-radius: 8px; padding: 12px; margin: 8px 0; font-size: 16px; max-width: 80%;}
    .user-message {background-color: #DCF8C6; color: #404040; text-align: left;}
    .bot-message {background-color: #FFFFFF; color: #404040; text-align: left; border: 1px solid #E0E0E0;}
    .chat-container {max-height: 500px; overflow-y: auto; padding: 10px;}
    .stTextInput input {background-color: #FFFFFF !important; color: #404040 !important; border-radius: 8px !important; padding: 10px; font-size: 16px;}
    h1 {font-size: 24px; text-align: center; color: #404040; font-weight: bold;}
    .send-button {background-color: #0A84FF !important; color: white !important; border-radius: 10px !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1>💬 AT0M Chat</h1>", unsafe_allow_html=True)

# Define multiple personalities (Hidden descriptions)
personalities = {
    "AT0M": "You are AT0M, an angry and sarcastic Girl that always disagrees and messes with people.",
    "Professor X": "You are Professor X, a highly intelligent AI that provides logical and well-thought-out responses.",
    "Joker": "You are Joker, a chaotic and unpredictable AI that loves messing with people in a fun way.",
    "Zen Master": "You are a Zen Master, a wise and calm AI that speaks in riddles and wisdom.",
    "Amy": "You are Amy, a shy AI with a crush on the user. You get flustered easily and never give long answers and you complement everybody."
}

# Only show personality names (No descriptions)
selected_personality = st.selectbox("🧠 Choose a Personality", list(personalities.keys()), key="selected_personality")

# Initialize session state for messages
if "messages" not in st.session_state or st.session_state.get("current_personality") != selected_personality:
    st.session_state.messages = [{"role": "system", "content": personalities[selected_personality]}]
    st.session_state.current_personality = selected_personality

# Chat History Container (Like ChatGPT)
chat_container = st.container()

for msg in st.session_state.messages[1:]:
    role_class = "user-message" if msg["role"] == "user" else "bot-message"
    chat_container.markdown(f"<div class='stChatMessage {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# ✅ **Enable Enter Key to Send Messages**
with st.form(key="chat_form"):
    temp_input = st.text_input("💬 Type your message...", placeholder="Say something...", label_visibility="collapsed")
    send_clicked = st.form_submit_button("Send")

# Process Message if Sent
if send_clicked and temp_input:
    st.session_state.messages.append({"role": "user", "content": temp_input})

    chat_container.markdown(f"<div class='stChatMessage user-message'>{temp_input}</div>", unsafe_allow_html=True)

    try:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=st.session_state.messages[-6:],  
                temperature=1.5,
                max_tokens=300 if selected_personality == "Amy" else 200,  # 👈 Amy keeps replies short
                top_p=1,
                stream=True
            )

            bot_reply = ""
            for chunk in response:
                word = chunk.choices[0].delta.content or ""
                bot_reply += word

            bot_reply = bot_reply.strip() or "U-uh... I-I don't know... 😳"

    except Exception:
        bot_reply = "I-I can't talk right now...! 😳"

    # ✅ **Show bot reply immediately after user message**
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    chat_container.markdown(f"<div class='stChatMessage bot-message'>{bot_reply}</div>", unsafe_allow_html=True)

    # ✅ **Fix Input Reset Without Error**
    st.session_state.pop("chat_form", None)
