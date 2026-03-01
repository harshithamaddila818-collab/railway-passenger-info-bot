
import streamlit as st
from groq import Groq
import time

# ✅ Secure API Key (DO NOT hardcode key here)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Railway Passenger Info Bot", page_icon="🚆", layout="wide")

# ----------------------------
# 🎨 Clean Modern UI Styling
# ----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(12px);
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: white;
}

.subtitle {
    text-align: center;
    color: #f1f1f1;
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #4f46e5;
    color: white;
    border-radius: 10px;
    padding: 8px 16px;
    transition: 0.3s ease;
    border: none;
}

.stButton>button:hover {
    background-color: #6366f1;
    transform: scale(1.05);
}

div[data-testid="stChatMessage"] {
    background-color: white;
    color: #1f2937;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🌍 Sidebar
# ----------------------------
with st.sidebar:
    st.title("🚆 Railway Info Bot")

    language = st.radio("🌐 Select Language:", ["English", "Telugu"])

    st.markdown("---")
    st.markdown("📋 Choose Category")

    category = st.selectbox(
        "Select Category:",
        ["-- Select --", 
         "🎟️ Ticket Related", 
         "🚉 Boarding Rules", 
         "🛤️ Platform System", 
         "🏢 Station Facilities"]
    )

    category_questions = {
        "🎟️ Ticket Related": [
            "Explain railway ticket types",
            "What is RAC in railway?",
            "What is waiting list?",
            "What is Tatkal ticket?",
            "Difference between sleeper and AC class"
        ],
        "🚉 Boarding Rules": [
            "Explain railway boarding rules",
            "When should I reach station?",
            "What documents are required?",
            "What happens if I miss train?",
            "Can I change boarding station?"
        ],
        "🛤️ Platform System": [
            "How does platform numbering work?",
            "Why do platforms change?",
            "How to know platform number?",
            "What if platform changes suddenly?"
        ],
        "🏢 Station Facilities": [
            "What facilities are available?",
            "Is WiFi available?",
            "What are waiting room facilities?",
            "What is cloak room service?",
            "Facilities for senior citizens?"
        ]
    }

    selected_question = None

    if category != "-- Select --":
        selected_question = st.selectbox(
            "Select Question:",
            ["-- Select Question --"] + category_questions[category]
        )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("👩‍💻 Developed by Harshitha")

# ----------------------------
# 🚆 Title
# ----------------------------
st.markdown('<div class="main-title">🚆 Railway Passenger Information Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask railway-related questions clearly and easily.</div>', unsafe_allow_html=True)

# ----------------------------
# 🚆 Quick Buttons
# ----------------------------
col1, col2, col3, col4 = st.columns(4)
quick_question = None

with col1:
    if st.button("🎟️ Ticket Types"):
        quick_question = "Explain railway ticket types"

with col2:
    if st.button("🚉 Boarding Rules"):
        quick_question = "Explain railway boarding rules"

with col3:
    if st.button("🛤️ Platform Info"):
        quick_question = "How does platform numbering work?"

with col4:
    if st.button("🏢 Station Facilities"):
        quick_question = "What facilities are available at railway stations?"

# ----------------------------
# 🧠 System Prompt
# ----------------------------
if language == "English":
    system_prompt = """
    You are a Railway Passenger Information Bot.
    Reply only in English.
    Explain only ticket types, boarding rules, platform usage, and station facilities.
    Do not book tickets or provide tracking.
    """
else:
    system_prompt = """
    మీరు Railway Passenger Information Bot.
    టికెట్ రకాల, బోర్డింగ్ నియమాలు, ప్లాట్‌ఫాం సమాచారం, స్టేషన్ సదుపాయాలు మాత్రమే వివరించండి.
    పూర్తిగా తెలుగులో సమాధానం ఇవ్వండి.
    """

# ----------------------------
# 💬 Chat Memory
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# 📝 Input Handling
# ----------------------------
typed_input = st.chat_input("Type your railway question here...")

user_input = None

if typed_input:
    user_input = typed_input
elif quick_question:
    user_input = quick_question
elif selected_question and selected_question != "-- Select Question --":
    user_input = selected_question

# ----------------------------
# 🤖 Generate Response (Typing Animation)
# ----------------------------
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("🚆 Generating response..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
        )

        reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for word in reply.split():
            full_response += word + " "
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.04)

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": reply})

# ----------------------------
# 🔻 Footer
# ----------------------------
st.markdown("---")
st.markdown(
    "<center style='color:white;'>🚆 Railway Passenger Information Bot | Built with ❤️ by Harshitha</center>",
    unsafe_allow_html=True
)