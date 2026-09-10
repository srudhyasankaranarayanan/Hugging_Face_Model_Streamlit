import streamlit as st
from huggingface_hub import InferenceClient

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #667eea 0%,
        #764ba2 35%,
        #f093fb 70%,
        #4facfe 100%
    );
}

/* Header */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: white;
    margin-top: 15px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: white;
    font-size: 18px;
    margin-bottom: 25px;
}

/* Welcome box */
.welcome {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    color: #333333;
    margin-bottom: 20px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
}

.welcome h3 {
    margin-bottom: 8px;
}

/* Chat messages */
.stChatMessage {
    border-radius: 15px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
}

/* Chat input */
.stChatInput {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown(
    '<div class="title">🤖 AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your intelligent AI assistant ✨</div>',
    unsafe_allow_html=True
)


# ---------------- HUGGING FACE ----------------
token = st.secrets["Access_Token"]

client = InferenceClient(
    api_key=token
)


# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I’m your AI Assistant. How can I help you today?"
        }
    ]


# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("🤖 AI Assistant")

    st.write("Your personal AI-powered assistant.")

    st.divider()

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hello! I’m your AI Assistant. How can I help you today?"
            }
        ]

        st.rerun()


# ---------------- WELCOME MESSAGE ----------------
if len(st.session_state.messages) == 1:

    st.markdown("""
    <div class="welcome">
        <h3>👋 Welcome!</h3>
        <p>
        I can help you with questions, explanations,
        coding, ideas, learning and much more.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- DISPLAY CHAT ----------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------- USER INPUT ----------------
question = st.chat_input(
    "💬 Ask your AI Assistant anything..."
)


# ---------------- PROCESS QUESTION ----------------
if question:

    # Display user message
    with st.chat_message("user"):

        st.markdown(question)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })


    # ---------------- AI RESPONSE ----------------
    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            messages = [

                {
                    "role": "system",
                    "content": """
                    You are a helpful, friendly and intelligent AI Assistant.

                    Your job is to:
                    - Answer questions clearly.
                    - Explain difficult topics simply.
                    - Help with programming and technical questions.
                    - Help with learning and projects.
                    - Provide useful suggestions when appropriate.
                    - Maintain context from the conversation.
                    - Never invent facts when information is unavailable.
                    - Be concise but informative.
                    """
                }

            ] + st.session_state.messages


            response = client.chat.completions.create(

                model="Qwen/Qwen3-4B-Thinking-2507",

                messages=messages
            )


            answer = response.choices[0].message.content

            st.markdown(answer)


    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })