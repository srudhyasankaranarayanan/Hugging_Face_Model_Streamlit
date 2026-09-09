import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="AI Question Answer",
    page_icon="🤖",
    layout="centered"
)

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

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: white;
    font-size: 18px;
    margin-bottom: 30px;
}

.question-label {
    color: white;
    font-size: 20px;
    font-weight: bold;
}

.answer-box {
    padding: 25px;
    border-radius: 18px;
    background-color: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.5);
    margin-top: 20px;
    color: #222222;
    font-size: 17px;
    line-height: 1.6;
    box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.15);
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

.stTextArea textarea {
    border-radius: 12px;
    font-size: 16px;
}

.answer-heading {
    color: white;
    font-size: 25px;
    font-weight: bold;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🤖 AI Question Answer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask anything and get an AI-powered answer ✨</div>',
    unsafe_allow_html=True
)

token = st.secrets["Access_Token"]

client = InferenceClient(
    api_key=token
)

st.markdown(
    '<div class="question-label">💬 Your Question</div>',
    unsafe_allow_html=True
)

question = st.text_area(
    "",
    placeholder="Type your question here...",
    height=120
)

if st.button("✨ Get Answer", use_container_width=True):

    if question.strip() == "":
        st.warning("⚠️ Please enter a question.")

    else:
        with st.spinner("🤔 AI is thinking..."):

            response = client.chat.completions.create(
                model="Qwen/Qwen3-4B-Thinking-2507",
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

        answer = response.choices[0].message.content

        st.markdown(
            '<div class="answer-heading">💡 AI Answer</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="answer-box">{answer}</div>',
            unsafe_allow_html=True
        )
