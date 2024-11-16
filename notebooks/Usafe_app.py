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

# User input field
user_input = st.text_input("Enter your request here:", placeholder="Type your question or concern...", key="user_input")

# Step 3: Handle user input
if user_input:
    # Acknowledge the user's input
    st.write("I’m truly sorry that you’ve gone through this. No one should ever face such treatment. Thank you for trusting me with your story.")

    # Step 4: Retrieve relevant documents from vector stores
    combined_results = retriever_combined.get_relevant_documents(user_input)
    general_results = retriever_general.get_relevant_documents(user_input)
    
    # Extract relevant definitions and laws
    if combined_results:
        hate_crime_def = combined_results[0].page_content
        st.write(f"Based on what you shared, it seems like you experienced a hate crime: {hate_crime_def}")
    
    if general_results:
        law_info = general_results[0].page_content
        st.write(f"This is illegal in Germany. Here’s one law that can protect you: {law_info}")
    
    # Step 5: Display options
    st.write("How would you like me to assist you further?")
    option = st.selectbox(
        "Choose one of the options below:",
        ("Select...", "Understanding Rights", "Steps to Report a Hate Crime", "Local Resources in Berlin", "General Information")
    )
    
    # Step 6: Handle user selection
    if option != "Select...":
        if option == "Understanding Rights":
            st.write("Retrieving information on your rights...")
            rights_info = retriever_general.get_relevant_documents("rights")[0].page_content
            st.write(rights_info)
        elif option == "Steps to Report a Hate Crime":
            st.write("Retrieving steps on how to report a hate crime...")
            report_info = retriever_general.get_relevant_documents("report")[0].page_content
            st.write(report_info)
        elif option == "Local Resources in Berlin":
            st.write("Retrieving local resources...")
            resources_info = retriever_general.get_relevant_documents("resources")[0].page_content
            st.write(resources_info)
        elif option == "General Information":
            st.write("Retrieving general information...")
            general_info = retriever_general.get_relevant_documents("general info")[0].page_content
            st.write(general_info)

