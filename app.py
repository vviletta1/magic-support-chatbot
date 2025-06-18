import streamlit as st
import cohere

# Load Cohere key securely from Streamlit secrets
co = cohere.Client(st.secrets["cohere_api_key"])

# Load support docs
with open("support_docs.txt", "r") as f:
    support_content = f.read()

# Streamlit UI
st.set_page_config(page_title="MagicSchool Support Chatbot")
st.title("📚 MagicSchool Support Chatbot")
st.markdown("Ask a question about using MagicSchool. This bot is trained on common support FAQs.")

# User input
query = st.text_input("Your question:")

if query:
    with st.spinner("Thinking..."):
        try:
            response = co.chat(
                message=query,
                documents=[
                    {"title": "MagicSchool Support Content", "snippet": support_content}
                ]
            )
            answer = response.text.strip()
            st.success(answer)

            # 🧠 Reference snippet (shows part of the context)
            st.markdown("**Reference Snippet:**")
            st.info(support_content[:300] + "...")

            # ✏️ Log interaction
            with open("support_log.txt", "a") as log:
                log.write(f"User: {query}\nBot: {answer}\n---\n")

            # 👍 User feedback
            st.markdown("**Was this helpful?**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Yes"):
                    st.info("Thanks for your feedback!")
            with col2:
                if st.button("👎 No"):
                    st.warning("Sorry! We’ll keep improving.")

        except Exception as e:
            st.error("Sorry, we’re having trouble answering that right now.")
            with open("support_log.txt", "a") as log:
                log.write(f"ERROR: {str(e)}\n---\n")