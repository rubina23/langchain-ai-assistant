import streamlit as st

from chatbot import final_chain


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
)


# -----------------------------
# Chat History
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Header
# -----------------------------

st.title("🤖 AI Assistant")
st.caption("Programming • Math • General")

st.write(
    "Ask a question and the AI will automatically "
    "choose the appropriate assistant."
)


# -----------------------------
# Display Previous Messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "user":
            st.write(message["content"])

        else:
            response = message["content"]

            st.write("### 💬 Answer")
            st.write(response["answer"])

            st.write("### 📋 Summary")
            st.write(response["summary"])

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Confidence",
                    f"{response['confidence']:.0%}"
                )

            with col2:
                st.metric(
                    "Category",
                    response["category"]
                )

            st.write("### 🔑 Keywords")

            if response["keywords"]:
                st.write(
                    " • ".join(response["keywords"])
                )


# -----------------------------
# User Input
# -----------------------------

question = st.chat_input(
    "Ask a Programming, Math, or General question..."
)


# -----------------------------
# Generate Response
# -----------------------------

if question:

    # Show user message immediately
    with st.chat_message("user"):
        st.write(question)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = final_chain.invoke({
                    "question": question
                })

                st.write("### 💬 Answer")
                st.write(response.answer)

                st.write("### 📋 Summary")
                st.write(response.summary)

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Confidence",
                        f"{response.confidence:.0%}"
                    )

                with col2:
                    st.metric(
                        "Category",
                        response.category
                    )

                st.write("### 🔑 Keywords")

                if response.keywords:
                    st.write(
                        " • ".join(response.keywords)
                    )

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": {
                        "answer": response.answer,
                        "summary": response.summary,
                        "confidence": response.confidence,
                        "category": response.category,
                        "keywords": response.keywords,
                    }
                })

            except Exception as e:

                st.error(
                    "Something went wrong while processing your question."
                )

                st.exception(e)


# -----------------------------
# Clear Chat
# -----------------------------

if st.session_state.messages:

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()