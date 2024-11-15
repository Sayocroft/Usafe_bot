import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

st.set_page_config(page_title="Usafe", page_icon=":safety_vest:")

# Load vector store
@st.cache_resource
def load_vector_store(path):
    """Load the FAISS vector store."""
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
    vector_store = FAISS.load_local(folder_path=path, embeddings=embedding_model, allow_dangerous_deserialization=True)
    return vector_store.as_retriever()

# Load both vector stores
st.write("Loading vector stores...")
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

# Step 4: Header and introduction

st.header(":safety_vest: Usafe - Your Anti-Discrimination Helpdesk")
st.write("Facing discrimination or hate? Get confidential support and essential guidance in seconds. Your Safety and Mental Health Matter")

def detect_hate_crime_type(inquiry, retrieval_chain=retriever_combined):
    """
    Detects the type of hate crime based on the user's inquiry using the 'usafe_combined' vector store.
    """
    # Ensure the input is a string before querying
    if isinstance(inquiry, dict):
        inquiry = inquiry.get("input", "")

    if not isinstance(inquiry, str):
        st.error("Invalid input. Please provide a valid text.")
        return "Unknown"
    
    # Query the combined vector store to find the most relevant example
    try:
        response = retrieval_chain.invoke({"input": inquiry})
    except Exception as e:
        st.error(f"Error querying vector store: {e}")
        return "Unknown"

    # Check if the response is a dictionary and contains 'answer'
    if isinstance(response, dict):
        # Extract the answer and ensure it's a string
        response_text = response.get('answer')
        if isinstance(response_text, str):
            # Process the extracted text to detect the type of hate crime
            if "discrimination" in response_text.lower():
                return "Discrimination"
            elif "hate speech" in response_text.lower():
                return "Hate Speech"
            elif "violence" in response_text.lower():
                return "Violence"
            else:
                return "Unknown"
        else:
            st.error("The response does not contain valid text.")
            return "Unknown"
    else:
        st.error("Invalid response format from vector store.")
        return "Unknown"

# User Input
user_input = st.text_area("Enter your inquiry:", placeholder="Describe the incident...")

if st.button("Submit"):
    if user_input.strip():
        detected_type = detect_hate_crime_type(user_input)
        st.write(f"**Detected Hate Crime Type:** {detected_type}")
    else:
        st.warning("Please enter a query.")


