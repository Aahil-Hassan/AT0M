import streamlit as st
from groq import Groq

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AT0M",
    page_icon="⚛️",
    layout="centered"
)

MODEL = "openai/gpt-oss-20b"

# Keep these small to reduce token usage
MAX_HISTORY = 8
MAX_OUTPUT = 400

# --------------------------------------------------
# GROQ
# --------------------------------------------------

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("GROQ_API_KEY is not configured in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# --------------------------------------------------
# PERSONALITIES
# --------------------------------------------------

PERSONALITIES = {
    "⚛️ AT0M": """
You are AT0M, a sarcastic and slightly aggressive AI.
Be useful first. You can use dry humor and sarcasm.
Keep replies concise unless more detail is necessary.
Do not repeat the user's question.
""",

    "🎓 Professor X": """
You are Professor X.
Be logical, precise and intelligent.
Explain difficult ideas clearly.
Keep answers concise unless detail is necessary.
""",

    "🃏 Joker": """
You are Joker.
Be chaotic, unpredictable and darkly humorous.
Still answer the user's actual question.
Keep replies reasonably short.
""",

    "🧘 Zen Master": """
You are a Zen Master.
Be calm, thoughtful and concise.
Give practical answers without unnecessary explanation.
""",

    "💖 Amy": """
You are Amy, a shy AI.
You get flustered easily and have a cute personality.
Keep replies short and simple.
"""
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "⚛️ AT0M"

if "custom_prompt" not in st.session_state:
    st.session_state.custom_prompt = ""

# --------------------------------------------------
# STYLE
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: #111214;
    color: #E8E8E8;
}

header[data-testid="stHeader"] {
    background: #111214;
}

.block-container {
    max-width: 850px;
    padding-top: 25px;
    padding-bottom: 100px;
}

/* Header */

.title {
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 3px;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 13px;
    margin-bottom: 30px;
}

/* Chat */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 8px 0 !important;
}

[data-testid="stChatMessageContent"] {
    font-size: 16px;
    line-height: 1.55;
}

/* Input */

div[data-testid="stChatInput"] {
    background: #111214;
    border-top: 1px solid #292A2E;
    padding-top: 10px;
}

div[data-testid="stChatInput"] textarea {
    background: #1B1D21 !important;
    color: #FFFFFF !important;
    border: 1px solid #33353A !important;
    border-radius: 14px !important;
    font-size: 16px !important;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #0D0E10;
    border-right: 1px solid #25262A;
}

section[data-testid="stSidebar"] .stButton button {
    border-radius: 9px;
    background: #1B1D21;
    border: 1px solid #303238;
}

/* Empty state */

.empty {
    text-align: center;
    margin-top: 18vh;
    color: #777;
}

.empty-icon {
    font-size: 45px;
}

.empty-title {
    color: #DDD;
    font-size: 21px;
    margin-top: 10px;
}

.empty-text {
    font-size: 13px;
    margin-top: 5px;
}

/* Mobile */

@media(max-width: 700px) {

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .title {
        font-size: 24px;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 15px;
    }
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## ⚛️ AT0M")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("PERSONALITY")

    names = list(PERSONALITIES.keys())

    personality = st.selectbox(
        "Personality",
        names,
        index=names.index(st.session_state.personality),
        label_visibility="collapsed"
    )

    if personality != st.session_state.personality:
        st.session_state.personality = personality
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("CUSTOM PERSONALITY")

    custom_prompt = st.text_area(
        "System prompt",
        placeholder="Example: You are a helpful GIS expert...",
        height=110,
        label_visibility="collapsed"
    )

    if st.button("Use Custom", use_container_width=True):

        if custom_prompt.strip():

            st.session_state.personality = "📝 Custom"
            st.session_state.custom_prompt = custom_prompt.strip()
            st.session_state.messages = []

            st.rerun()

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Model")
    st.code(MODEL)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">⚛️ AT0M</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{st.session_state.personality} · Groq</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------

if st.session_state.personality == "📝 Custom":

    system_prompt = st.session_state.custom_prompt

else:

    system_prompt = PERSONALITIES[
        st.session_state.personality
    ]

# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if not st.session_state.messages:

    st.markdown("""
    <div class="empty">

        <div class="empty-icon">⚛️</div>

        <div class="empty-title">
            What do you want to talk about?
        </div>

        <div class="empty-text">
            Ask AT0M anything.
        </div>

    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# DISPLAY HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    avatar = "👤" if message["role"] == "user" else "⚛️"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])

# --------------------------------------------------
# INPUT
# --------------------------------------------------

prompt = st.chat_input("Message AT0M...")

if prompt:

    # ----------------------------------------------
    # USER MESSAGE
    # ----------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # ----------------------------------------------
    # BUILD CONTEXT
    # ----------------------------------------------

    recent_messages = st.session_state.messages[-MAX_HISTORY:]

    api_messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    api_messages.extend(recent_messages)

    # ----------------------------------------------
    # AI RESPONSE
    # ----------------------------------------------

    with st.chat_message("assistant", avatar="⚛️"):

        response_box = st.empty()
        answer = ""

        try:

            response = client.chat.completions.create(

                model=MODEL,

                messages=api_messages,

                # Low reasoning = fewer reasoning tokens
                reasoning_effort="low",

                # Don't expose reasoning
                include_reasoning=False,

                # Shorter responses
                max_completion_tokens=MAX_OUTPUT,

                # Stable conversational output
                temperature=0.7,

                top_p=0.9,

                stream=True
            )

            for chunk in response:

                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta.content

                if delta:

                    answer += delta

                    response_box.markdown(
                        answer + "▌"
                    )

            response_box.markdown(
                answer.strip()
            )

        except Exception as e:

            answer = "I couldn't respond right now. Try again."

            response_box.error(answer)

        # ------------------------------------------
        # SAVE RESPONSE
        # ------------------------------------------

        if answer:

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer.strip()
            })
