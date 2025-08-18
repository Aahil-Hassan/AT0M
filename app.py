import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Page Config
st.set_page_config(page_title="AT0M Chat", page_icon="💬", layout="wide")

st.markdown(
    """
    <style>
    /* Global Dark Theme */
    .stApp {
        background-color: #121212 !important;
        color: #EAEAEA !important;
        font-size: 18px !important;
    }
    html, body, [class*="css"] {
        background-color: #121212 !important;
        color: #EAEAEA !important;
    }

    /* Remove top white header space */
    header[data-testid="stHeader"], div[data-testid="stToolbar"] {
        background-color: #121212 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0F1117 !important;
        padding: 10px !important;
    }
    section[data-testid="stSidebar"] * {
        color: #EAEAEA !important;
    }

    /* Sidebar Personality Buttons */
    section[data-testid="stSidebar"] .stButton>button {
        width: 100%;
        background: #2C2F36;
        border: 1px solid #333;
        color: #EAEAEA;
        border-radius: 12px;
        padding: 12px;
        font-size: 18px;
        margin-bottom: 6px;
        transition: all 0.2s ease-in-out;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background: #3A3D44;
        border-color: #555;
    }
    .sidebar-pill {
        background: linear-gradient(135deg, #3A3D44, #2C2F36);
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 18px;
        margin-bottom: 8px;
        color: #FFFFFF !important;
    }

    /* Title */
    h1 {
        font-size: 32px;
        text-align: center;
        color: #EAEAEA;
        font-weight: 700;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    /* Chat Container */
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding: 8px;
        margin-bottom: 80px; /* leave space for sticky input */
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 14px;
        padding: 14px 18px;
        margin: 10px 0;
        font-size: 18px;
        line-height: 1.5;
        max-width: 85%;
        word-wrap: break-word;
        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }
    .user-message {
        background-color: #2C2F36;
        color: #FFFFFF;
        margin-left: auto;
    }
    .bot-message {
        background-color: #1E1F24;
        color: #EAEAEA;
        border: 1px solid #333;
        margin-right: auto;
    }

    /* Chat Input Sticky */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        background-color: #121212 !important;
        padding: 12px 16px !important;
        z-index: 1000 !important;
        border-top: 1px solid #2C2F36;
    }
    
    div[data-testid="stChatInput"] textarea {
        background-color: #1E1F24 !important;
        color: #FFFFFF !important;
        font-size: 18px !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        resize: none !important;
    }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        h1 { font-size: 24px !important; }
        .stChatMessage { font-size: 16px !important; padding: 12px 14px !important; }
        section[data-testid="stSidebar"] .stButton>button,
        .sidebar-pill { font-size: 16px !important; padding: 10px !important; }
        div[data-testid="stChatInput"] textarea { font-size: 16px !important; padding: 10px !important; }
    }
    /* Custom Personality TextArea (Sidebar) */
    section[data-testid="stSidebar"] textarea {
        background-color: #1E1F24 !important;  /* dark background */
        color: #EAEAEA !important;             /* light text */
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        padding: 10px !important;
        font-size: 16px !important;
        resize: none !important;
        box-shadow: none !important;
    }

    /* Custom Personality Placeholder */
    section[data-testid="stSidebar"] textarea::placeholder {
        color: #888 !important;
    }



    /* Scrollbar Styling */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1E1F24; }
    ::-webkit-scrollbar-thumb { background: #444; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #666; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1>💬 AT0M Chat</h1>", unsafe_allow_html=True)

personalities = {
    "🤖 AT0M": "You are AT0M, an angry and sarcastic Girl that always disagrees , insluts and curse.",
    "🎓 Professor X": "You are Professor X, logical and intelligent.",
    "🃏 Joker": "You are Joker, chaotic and unpredictable. even you dont know what you are doing",
    "🧘 Zen Master": "You are a Zen Master, wise and calm.",
    "💖 Amy": "You are Amy, a shy AI that gets flustered easily and keeps replies short."
}

with st.sidebar:
    st.markdown("### 🧠 Choose a Personality")

    if "selected_personality" not in st.session_state:
        st.session_state.selected_personality = "🤖 AT0M"

    for name in personalities.keys():
        if st.session_state.selected_personality == name:
            st.markdown(f"<div class='sidebar-pill'>{name}</div>", unsafe_allow_html=True)
        else:
            if st.button(name, key=f"btn_{name}"):
                st.session_state.selected_personality = name
                st.session_state.messages = [{"role": "system", "content": personalities[name]}]
                st.session_state.current_personality = name
                st.rerun()

    st.markdown("---")
    st.markdown("### ✍️ Custom Personality")
    custom_text = st.text_area("Write your own system prompt here:", key="custom_persona_input", height=100)

    if st.button("Activate Custom Personality"):
        if custom_text.strip():
            st.session_state.selected_personality = "📝 Custom"
            st.session_state.messages = [{"role": "system", "content": custom_text.strip()}]
            st.session_state.current_personality = "📝 Custom"
            st.rerun()

selected_personality = st.session_state.selected_personality

if "messages" not in st.session_state or st.session_state.get("current_personality") != selected_personality:
    if selected_personality in personalities:
        st.session_state.messages = [{"role": "system", "content": personalities[selected_personality]}]
    else:  # Custom personality
        st.session_state.messages = [{"role": "system", "content": st.session_state.get("custom_persona_input", "You are a helpful assistant.")}]
    st.session_state.current_personality = selected_personality

if "messages" not in st.session_state or st.session_state.get("current_personality") != selected_personality:
    st.session_state.messages = [{"role": "system", "content": personalities[selected_personality]}]
    st.session_state.current_personality = selected_personality

# Chat history
chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.messages[1:]:
        role_class = "user-message" if msg["role"] == "user" else "bot-message"
        icon = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(
            f"""
            <div class='stChatMessage {role_class}'>
                <div class='msg-icon'>{icon}</div>
                <div class='msg-text'>{msg['content']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

user_input = st.chat_input(placeholder="💬 Type your message here...", key="chatbox")


if user_input:
    # show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    chat_container.markdown(f"<div class='stChatMessage user-message'>{user_input}</div>", unsafe_allow_html=True)

    try:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=st.session_state.messages[-10:],   # keep context tight
                temperature=1.2,
                max_tokens=600 if "Amy" not in selected_personality else 250,
                top_p=1,
                stream=True
            )

            # stream bot text
            bot_reply = ""
            with chat_container:
                placeholder = st.empty()
            for chunk in response:
                delta = chunk.choices[0].delta.content or ""
                bot_reply += delta
                placeholder.markdown(
                    f"<div class='stChatMessage bot-message'>{bot_reply}▌</div>",
                    unsafe_allow_html=True
                )
            placeholder.markdown(
                f"<div class='stChatMessage bot-message'>{bot_reply.strip() or '…'}</div>",
                unsafe_allow_html=True
            )

    except Exception:
        bot_reply = "Hmm, I can’t respond right now."
        chat_container.markdown(f"<div class='stChatMessage bot-message'>{bot_reply}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

