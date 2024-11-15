import streamlit as st
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import os
from langchain.chains import RetrievalQA

# Step 0: API

os.environ["GROQ_API_KEY"] = "sk_CZ8i7Axljvq4EEUxEybdWGdyb3FYxTnafeQGz4Ydl98fqV20gnzF"



# Step 4: Header and intro text

st.image("https://emojicdn.elk.sh/safety_vest", use_column_width=True)
st.set_page_config(page_title="Usafe", page_icon=":safety_vest:")

st.header(":safety_vest: Usafe - Your Anti-Discrimination Helpdesk")
st.write("Facing discrimination or hate? Get confidential support and essential guidance in seconds. Your Safety and Mental Health Matter")


# Step 5: User input

user_input = st.text_area("Describe your situation:", height=150)

if st.button("Submit") and user_input.strip():
    with st.spinner("Analyzing..."):
        # Step 1: Detect the type of hate crime
        crime_type_response = hate_crime_chain.run(user_input)
        st.subheader("Detected Hate Crime Type")
        st.write(crime_type_response)

        # Step 2: Provide options for further guidance
        st.subheader("Available Options")
        option = st.selectbox(
            "Select an option for further guidance:",
            [
                "Understanding your rights in German",
                "How to report a crime in Germany",
                "General information",
                "Local resources",
                "Something else"
            ]
        )

