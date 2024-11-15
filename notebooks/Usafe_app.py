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

# Check if the vector stores are loaded correctly
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

# Step 3: User query input
query = st.text_input("Enter your question:")


# Step 4: Display results from the appropriate vector store
if query:
    st.write("Searching in the general knowledge base...")
    general_response = retriever_general.get_relevant_documents(query)
    
    st.write("Searching in the specific hate crime database...")
    combined_response = retriever_combined.get_relevant_documents(query)
    
    # Display results from the general vector store
    st.subheader("General Information")
    for i, doc in enumerate(general_response):
        st.write(f"{i + 1}. {doc['text']}")

    # Display results from the combined vector store
    st.subheader("Specific Hate Crime Information")
    for i, doc in enumerate(combined_response):
        st.write(f"{i + 1}. {doc['text']}")

