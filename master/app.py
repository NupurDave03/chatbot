import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cleardeals FAQ Chatbot", page_icon="🤖", layout="centered")
st.markdown(
    """
    <style>
    .main {background: linear-gradient(145deg, #e0eafc 0%, #cfdef3 100%) !important;}
    .stChatMessage.user {background: #fffcf7; color: #7b4c15; border-radius: 18px 18px 0 18px;}
    .stChatMessage.bot {background: #eaf6ff; color: #34568b; border-radius: 18px 18px 18px 0;}
    .suggested-q {display:inline-block;margin:7px 9px 7px 0;padding:9px 18px;background:#f4faff;border-radius:18px;cursor:pointer;font-size:1rem;transition:.2s;}
    .suggested-q:hover {background:#d7e3fc;color:#4d68a1;box-shadow:0 1px 7px #6ab8f822;}
    .stTextInput > div > div > input {font-size:1.14rem;}
    </style>
    """, unsafe_allow_html=True
)

st.markdown("## 🤖 Cleardeals Hiring & Training Chatbot")
st.markdown(
    "Type your question, or tap a suggested question below. \
    <br><br>", unsafe_allow_html=True)

faq = pd.read_csv('hiring_training_faq.csv')

# --- Answer Matching Logic ---
def get_best_answer(user_query):
    import datetime
    uq = user_query.strip().lower()
    # FAQ matching first
    for _, row in faq.iterrows():
        if uq == row['Question'].strip().lower():
            return row['Answer']
    for _, row in faq.iterrows():
        if uq in row['Question'].strip().lower():
            return row['Answer']
    uq_words = set(uq.split())
    for _, row in faq.iterrows():
        q_words = set(row['Question'].strip().lower().split())
        if uq_words & q_words:
            return row['Answer']

    # Basic greetings
    greetings = {
        "hi": "Hello! How can I help you today?",
        "hello": "Hi there! How can I assist you?",
        "hey": "Hey! What would you like to know?",
        "good morning": "Good morning! How can I help you today?",
        "good afternoon": "Good afternoon! How can I help you today?",
        "good evening": "Good evening! How can I help you today?",
        "bye": "Goodbye! Have a great day!",
        "thank you": "You're welcome! If you have more questions, just ask.",
        "thanks": "You're welcome!",
        "how are you": "I'm just a bot, but I'm here to help you!",
        "what's up": "I'm here to answer your questions about hiring and training at Cleardeals!",
        "how's your day": "I'm always ready to help you!",
        "how are you doing": "I'm doing well, thank you! How can I help you?",
        "good night": "Good night! Feel free to ask more questions anytime.",
        "see you": "See you! Come back if you have more questions."
    }
    for key, value in greetings.items():
        if key in uq:
            return value
    # Time-based greeting
    if "good" in uq and ("morning" in uq or "afternoon" in uq or "evening" in uq or "night" in uq):
        hour = datetime.datetime.now().hour
        if hour < 12:
            return "Good morning! How can I help you today?"
        elif hour < 17:
            return "Good afternoon! How can I help you today?"
        elif hour < 21:
            return "Good evening! How can I help you today?"
        else:
            return "Good night! Feel free to ask more questions anytime."
    # Mood questions
    if "how are you" in uq or "how do you feel" in uq or "your mood" in uq:
        return "I'm just a bot, but I'm always happy to help!"
    return "Sorry, I couldn't find an answer to that. Please contact HR for more help."

# --- Suggested Questions ---
suggested_questions = faq['Question'].tolist()[:7]  # Show first 7 as main suggestions

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "bot", "msg": "Welcome! Ask me anything about hiring or training at Cleardeals, or tap a suggested question below 👇"}
    ]

def add_message(role, msg):
    st.session_state.chat_history.append({"role": role, "msg": msg})

with st.container():
    # Show chat messages
    for m in st.session_state.chat_history:
        align = "user" if m["role"] == "user" else "bot"
        st.chat_message(align).write(m["msg"])

input_container = st.container()
col1, col2 = st.columns([6, 1])

with input_container:
    with col1:
        user_input = st.text_input("You:", value="", placeholder="Type your question...", key="user_input", label_visibility="collapsed")
    with col2:
        send_btn = st.button('Send', use_container_width=True)

# --- Suggested Questions UI ---
st.markdown("<div style='margin-bottom:15px;'></div><b>Suggested questions:</b><br>", unsafe_allow_html=True)
ssq_cols = st.columns(len(suggested_questions))
for i, q in enumerate(suggested_questions):
    if ssq_cols[i].button(q, key=f"qbtn_{i}", help="Click to ask this"):
        add_message("user", q)
        answer = get_best_answer(q)
        add_message("bot", answer)
        st.rerun()

# --- Handle User Input ---
if send_btn and user_input.strip():
    add_message("user", user_input)
    answer = get_best_answer(user_input)
    add_message("bot", answer)
    st.rerun()
