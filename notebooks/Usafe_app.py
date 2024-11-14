import streamlit as st
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import os

# Step 0: API

os.environ["GROQ_API_KEY"] = "sk_CZ8i7Axljvq4EEUxEybdWGdyb3FYxTnafeQGz4Ydl98fqV20gnzF"

# Step 1: Initialize Llama Model
llama_model = ChatGroq(model="llama3-8b-8192")

# Step 2: Load Vector Stores
combined_vector_store = FAISS.load_local("usafe_combined")
general_vector_store = FAISS.load_local("usafe_general")


# Step 3: Initialize Chains for both vector stores
combined_chain = RetrievalQA.from_chain_type(
    llm=llama_model,
    chain_type="stuff",
    retriever=combined_vector_store.as_retriever()
)

general_chain = RetrievalQA.from_chain_type(
    llm=llama_model,
    chain_type="stuff",
    retriever=general_vector_store.as_retriever()
)

# Step 4: Header and intro text


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

