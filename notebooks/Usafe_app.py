import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Usafe", page_icon=":safety_vest:")

# Get the API key from environment variables
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API Key not found. Please check your .env file.")
    st.stop()

# Initialize the ChatGroq client
llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=api_key
)

# Load vector store
@st.cache_resource
def load_vector_store(path):
    """Load the FAISS vector store."""
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
    vector_store = FAISS.load_local(folder_path=path, embeddings=embedding_model, allow_dangerous_deserialization=True)
    return vector_store.as_retriever()


# Load both vector stores
retriever_combined = load_vector_store('notebooks/vector_databases/usafe_combined')
retriever_general = load_vector_store('notebooks/vector_databases/usafe_general')

# Check if the vector stores are loaded correctly (delete later for the demo)
if retriever_combined:
    st.success("Loaded 'usafe_combined' vector store successfully.")
    st.write(f"Number of documents in 'usafe_combined': {retriever_combined.vectorstore.index.ntotal}")
else:
    st.error("Failed to load 'usafe_combined' vector store.")

if retriever_general:
    st.success("Loaded 'usafe_general' vector store successfully.")
    st.write(f"Number of documents in 'usafe_general': {retriever_general.vectorstore.index.ntotal}")
else:
    st.error("Failed to load 'usafe_general' vector store.")

st.title(":safety_vest: Usafe - Your Anti-Discrimination Helpdesk")

st.write("Facing discrimination or hate? Get confidential support and essential guidance in seconds. Your Safety and Mental Health Matter")

# User input: Description of the incident
user_input = st.text_area("Please describe what happened to you", height=150)

if st.button("Detect Hate Crime"):
    if user_input:
        try:
            # Step 1: Detect the hate crime type using `invoke()`
            hate_crime_response = retriever_combined.invoke(
                {"input": f"Please classify the following incident description:\n'{user_input}'"}
            )

            # Extract the detected hate crime type from the response
            detected_hate_crime = hate_crime_response.get('result', {}).get('content', "Unknown")
            
            # Display the detected type
            st.write(f"Detected Hate Crime Type: **{detected_hate_crime}**")

        except Exception as e:
            st.error(f"Error in detecting hate crime: {e}")






