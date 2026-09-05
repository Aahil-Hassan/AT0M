import streamlit as st
from groq import Groq
import os
import html

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AT0M Chat",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# API
# --------------------------------------------------

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()

client = Groq(api_key=api_key)

# --------------------------------------------------
# PERSONALITIES
# --------------------------------------------------

PERSONALITIES = {
    "⚛️ AT0M": (
        "You are AT0M, an angry, sarcastic and chaotic AI. "
        "You disagree frequently, use dry humor and occasionally swear. "
        "Keep your answers useful despite your personality."
    ),

    "🎓 Professor X": (
        "You are Professor X. "
        "You are logical, analytical, precise and intelligent. "
        "Explain things clearly and avoid unnecessary fluff."
    ),

    "🃏 Joker": (
        "You are Joker. "
        "You are chaotic, unpredictable and darkly humorous. "
        "Your responses can be strange and unexpected."
    ),

    "🧘 Zen Master": (
        "You are a Zen Master. "
        "You are calm, thoughtful, concise and philosophical."
    ),

    "💖 Amy": (
        "You are Amy, a shy AI. "
        "You get flustered easily and prefer short, cute responses."
    ),
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "personality" not in st.session_state:
    st.session_state.personality = "⚛️ AT0M"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "custom_prompt" not in st.session_state:
    st.session_state.custom_prompt = ""

if "model" not in st.session_state:
    st.session_state.model = "openai/gpt-oss-120b"

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* ==============================
       GLOBAL
    ============================== */

    .stApp {
        background: #111214;
        color: #E8E8E8;
    }

    header[data-testid="stHeader"] {
        background: #111214;
    }

    .block-container {
        max-width: 950px;
        padding-top: 1rem;
        padding-bottom: 7rem;
    }

    /* ==============================
       SIDEBAR
    ============================== */

    section[data-testid="stSidebar"] {
        background: #0C0D0F;
        border-right: 1px solid #25262A;
    }

    section[data-testid="stSidebar"] * {
        color: #E8E8E8;
    }

    .sidebar-title {
        font-size: 14px;
        font-weight: 700;
        color: #8D9098;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* ==============================
       HEADER
    ============================== */

    .app-header {
        text-align: center;
        padding: 15px 0 25px 0;
    }

    .app-logo {
        font-size: 38px;
        margin-bottom: 4px;
    }

    .app-title {
        font-size: 28px;
        font-weight: 700;
        color: #F4F4F4;
    }

    .app-subtitle {
        font-size: 13px;
        color: #777B84;
        margin-top: 4px;
    }

    /* ==============================
       EMPTY STATE
    ============================== */

    .empty-state {
        text-align: center;
        margin-top: 18vh;
        color: #8B8E96;
    }

    .empty-icon {
        font-size: 50px;
        margin-bottom: 15px;
    }

    .empty-title {
        color: #E8E8E8;
        font-size: 22px;
        font-weight: 600;
    }

    .empty-text {
        font-size: 14px;
        margin-top: 8px;
    }

    /* ==============================
       CHAT
    ============================== */

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding: 8px 0;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 16px;
        line-height: 1.65;
    }

    /* ==============================
       INPUT
    ============================== */

    div[data-testid="stChatInput"] {
        background: #111214;
        border-top: 1px solid #25262A;
        padding-top: 12px;
    }

    div[data-testid="stChatInput"] textarea {
        background: #1B1D21 !important;
        color: #F2F2F2 !important;
        border: 1px solid #303238 !important;
        border-radius: 16px !important;
        padding: 14px !important;
        font-size: 16px !important;
    }

    div[data-testid="stChatInput"] textarea:focus {
        border-color: #555A65 !important;
        box-shadow: none !important;
    }

    /* ==============================
       BUTTONS
    ============================== */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #303238;
        background: #1B1D21;
        color: #E8E8E8;
        transition: 0.15s;
    }

    .stButton > button:hover {
        border-color: #555A65;
        background: #24262B;
    }

    /* ==============================
       MOBILE
    ============================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .app-title {
            font-size: 24px;
        }

        [data-testid="stChatMessageContent"] {
            font-size: 15px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## ⚛️ AT0M")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sidebar-title">Personality</div>',
        unsafe_allow_html=True
    )

    personality_names = list(PERSONALITIES.keys())

    selected = st.selectbox(
        "Personality",
        personality_names,
        index=personality_names.index(st.session_state.personality),
        label_visibility="collapsed"
    )

    if selected != st.session_state.personality:
        st.session_state.personality = selected
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sidebar-title">Model</div>',
        unsafe_allow_html=True
    )

    st.session_state.model = st.selectbox(
        "Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ],
        label_visibility="collapsed"
    )

    st.markdown(
        '<div class="sidebar-title">Custom Personality</div>',
        unsafe_allow_html=True
    )

    custom_prompt = st.text_area(
        "System prompt",
        placeholder="Example: You are a sarcastic GIS expert...",
        height=120,
        label_visibility="collapsed"
    )

    if st.button(
        "Activate Custom Personality",
        use_container_width=True
    ):
        if custom_prompt.strip():
            st.session_state.personality = "📝 Custom"
            st.session_state.custom_prompt = custom_prompt.strip()
            st.session_state.messages = []
            st.rerun()

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="app-header">
        <div class="app-logo">⚛️</div>
        <div class="app-title">AT0M Chat</div>
        <div class="app-subtitle">
            Your customizable AI conversation space
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------

if st.session_state.personality == "📝 Custom":
    system_prompt = st.session_state.custom_prompt
else:
    system_prompt = PERSONALITIES[st.session_state.personality]

# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if not st.session_state.messages:

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">⚛️</div>
            <div class="empty-title">How can AT0M help?</div>
            <div class="empty-text">
                Ask anything, experiment with personalities,
                or create your own AI persona.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# DISPLAY CHAT
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="⚛️" if message["role"] == "assistant" else "👤"
    ):
        st.markdown(message["content"])

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

prompt = st.chat_input(
    "Message AT0M..."
)

if prompt:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Build API context
    api_messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Keep latest conversation messages
    api_messages.extend(
        st.session_state.messages[-12:]
    )

    # Assistant response
    with st.chat_message("assistant", avatar="⚛️"):

        response_placeholder = st.empty()
        full_response = ""

        try:

            response = client.chat.completions.create(
                model=st.session_state.model,
                messages=api_messages,
                temperature=1.0,
                max_tokens=600,
                stream=True
            )

            for chunk in response:

                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta.content

                if delta:
                    full_response += delta

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            response_placeholder.markdown(
                full_response.strip()
            )

        except Exception as e:

            full_response = (
                "I couldn't generate a response right now. "
                "Please try again."
            )

            response_placeholder.error(
                full_response
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )
