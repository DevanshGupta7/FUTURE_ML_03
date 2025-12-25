import streamlit as st
import requests
from dotenv import load_dotenv
import os

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.chat-container {
    max-width: 850px;
    margin: auto;
    margin-top: 1rem;
}

.block-container {
    padding-top: 2rem !important;
}

.user-row {
    display: flex;
    justify-content: flex-end;
}

.bot-row {
    display: flex;
    justify-content: flex-start;
}

.user-msg {
    background: #1f6feb;
    color: white;
    padding: 12px 16px;
    border-radius: 16px 16px 4px 16px;
    margin: 6px 0;
    max-width: 70%;
}

.bot-msg {
    background: #161b22;
    color: #e6edf3;
    padding: 12px 16px;
    border-radius: 16px 16px 16px 4px;
    margin: 6px 0;
    max-width: 70%;
    border: 1px solid #30363d;
}

.avatar {
    font-size: 20px;
    margin: 0 8px;
}

.order-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 12px;
    margin-top: 6px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "bot_pending" not in st.session_state:
    st.session_state.bot_pending = False

load_dotenv(override=True)
BACKEND_URL = os.getenv("BACKEND_URL")

if not BACKEND_URL:
    st.error("❌ BACKEND_URL not set")
    st.stop()

st.title("💬 Customer Support Chatbot")
st.caption(f"Backend: {BACKEND_URL}")

col1, col2 = st.columns([8, 2])

with col2:
    if st.button("🗑 Reset Chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for sender, text in st.session_state.messages:
    if sender == "You":
        st.markdown(f"""
        <div class="user-row">
            <div class="user-msg">{text}</div>
            <div class="avatar">👤</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-row">
            <div class="avatar">🤖</div>
            <div class="bot-msg">{text}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

msg = st.chat_input("Ask anything")

if msg:
    st.session_state.messages.append(("You", msg))
    st.session_state.bot_pending = True
    st.rerun()

if st.session_state.bot_pending:
    typing_placeholder = st.empty()
    typing_placeholder.markdown(
        """
        <div class="bot-row">
            <div class="avatar">🤖</div>
            <div class="bot-msg">⏳ Bot is typing...</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    last_user_msg = next(
        msg for msg in reversed(st.session_state.messages)
        if msg[0] == "You"
    )[1]

    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={"text": last_user_msg},
        timeout=10
    )

    if response.status_code == 200:
        bot_reply = response.json().get("reply", "No response")
    else:
        bot_reply = "❌ Server error"

    typing_placeholder.empty()

    st.session_state.messages.append(("Bot", bot_reply))
    st.session_state.bot_pending = False
    st.rerun()