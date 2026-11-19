
import io
import streamlit as st
from groq import generate_response

# Page configuration
st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.question {
    color: #0876c9;
    font-weight: bold;
    font-size: 18px;
}
.answer {
    line-height: 1.7;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)


# Export conversation history
def export_bytes(history):
    text = ""

    for i, item in enumerate(history, 1):
        text += f"Q{i}: {item['question']}\n"
        text += f"A{i}: {item['answer']}\n\n"

    return io.BytesIO(text.encode("utf-8"))


# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []


# Main heading
st.title("🤖 AI Teaching Assistant")

st.write(
    "Ask me anything about various subjects, "
    "and I'll provide an insightful answer."
)

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.history = []
        st.rerun()

with col2:
    if st.session_state.history:
        st.download_button(
            "📤 Export Chat History",
            data=export_bytes(st.session_state.history),
            file_name="AI_Teaching_Assistant_History.txt",
            mime="text/plain",
            use_container_width=True
        )


# Question input
st.subheader("Ask a Question")

with st.form("question_form"):
    user_input = st.text_input(
        "Enter your question here:",
        placeholder="e.g. Who was Chaudhry Rehmat Ali?"
    )

    ask = st.form_submit_button("Ask")


# Generate answer
if ask:
    question = user_input.strip()

    if not question:
        st.warning("Please enter a question first.")

    else:
        try:
            with st.spinner("🤖 Generating your answer..."):

                answer = generate_response(
                    question,
                    temperature=0.3,
                    max_tokens=1024
                )

            if not answer:
                answer = "The AI returned an empty response. Please try again."

            st.session_state.history.insert(
                0,
                {
                    "question": question,
                    "answer": answer
                }
            )

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")


# Conversation history
st.divider()
st.header("📚 Conversation History")

if not st.session_state.history:

    st.info("Your questions and answers will appear here.")

else:

    for i, item in enumerate(st.session_state.history, 1):

        with st.expander(
            f"Q{i}: {item['question']}",
            expanded=(i == 1)
        ):

            st.markdown("### 🤖 AI Answer")

            if item["answer"].startswith(
                ("Error:", "All Groq models failed", "Groq model failed")
            ):
                st.error(item["answer"])
            else:
                st.markdown(item["answer"])


