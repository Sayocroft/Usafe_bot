import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import create_stuff_documents_chain, create_retrieval_chain

# Load environment variables
load_dotenv()

# Define the hate crimes types
HATE_CRIMES_TYPE = {
    'anti_religious_def.pdf': 'Anti-religious Hate Crime',
    'racist_def.pdf': 'Racist and Xenophobic Hate Crime',
    'gender_lgbt_def.pdf': 'Gender and LGBTQ+ Hate Crime'
}

st.set_page_config(page_title="Usafe", page_icon=":safety_vest:")

# Step 1: Initialize the ChatGroq LLM
def initialize_llm(model_name="llama3-8b-8192"):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("API Key not found. Please check your .env file.")
        st.stop()
    return ChatGroq(
        model=model_name,
        api_key=api_key,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

llm = initialize_llm()

# Step 2: Load vector stores
@st.cache_resource
def load_vector_store(path):
    """Load the FAISS vector store."""
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
    vector_store = FAISS.load_local(folder_path=path, embeddings=embedding_model, allow_dangerous_deserialization=True)
    return vector_store.as_retriever()

# Load both vector stores
retriever_combined = load_vector_store('notebooks/vector_databases/usafe_combined')
retriever_general = load_vector_store('notebooks/vector_databases/usafe_general')

# Step 3: Connect Chains (LLM + Vector Store)
def connect_chains(retriever):
    """
    Connects the retriever with the LLM using a retrieval chain.
    """
    stuff_documents_chain = create_stuff_documents_chain(
        llm=llm,
        prompt="Provide a helpful response based on the retrieved documents."
    )
    retrieval_chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=stuff_documents_chain
    )
    return retrieval_chain

# Create chains for both general and combined retrievals
general_chain = connect_chains(retriever_general)
combined_chain = connect_chains(retriever_combined)

# Step 4: Streamlit UI Setup
st.title(":safety_vest: Usafe - Your Anti-Discrimination Helpdesk")
st.write("Facing discrimination or hate? Get confidential support and essential guidance in seconds. Your safety and mental health matter.")

# Step 5: Initialize session state for tracking form submissions
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# Step 6: Define the user form for input
with st.form(key="user_form"):
    user_input = st.text_input("Describe briefly what happened to you:", placeholder="Type here...", key="user_input")
    submit_button = st.form_submit_button(label="Submit")

# Function to retrieve documents with metadata filtering
def get_relevant_info_with_metadata(query, section_filter=None, k=5):
    """
    Retrieve relevant information with metadata filtering.
    """
    search_kwargs = {'k': k}
    if section_filter:
        search_kwargs['metadata_filter'] = {"section": section_filter}
    results = retriever_general.get_relevant_documents(query, search_kwargs=search_kwargs)
    if results:
        full_content = " ".join([result.page_content.strip() for result in results if result.page_content])
        return full_content if full_content else "No information available."
    return "No information found."

# Step 7: Handle form submission
if submit_button:
    st.session_state['submitted'] = True

# Step 8: Process user input and generate response
if st.session_state['submitted'] and st.session_state['user_input']:
    st.markdown("### I’m truly sorry that you’ve gone through this.")
    st.markdown("No one should ever face such treatment. Thank you for trusting me with your story.")

    # Retrieve relevant documents from the combined vector store to identify hate crime type
    combined_results = combined_chain.run(st.session_state['user_input'])
    
    # Determine the type of hate crime
    hate_crime_type = None
    if combined_results:
        hate_crime_source = combined_results[0].metadata.get('source')
        if hate_crime_source:
            if "anti_religious_def.pdf" in hate_crime_source:
                hate_crime_type = "Anti-Religious Hate Crime"
                st.write("🛑 You experienced an **Anti-Religious Hate Crime**.")
            elif "racist_def.pdf" in hate_crime_source:
                hate_crime_type = "Racist and Xenophobic Hate Crime"
                st.write("🛑 You experienced a **Racist and Xenophobic Hate Crime**.")
            elif "gender_lgbt_def.pdf" in hate_crime_source:
                hate_crime_type = "Gender and LGBTQ+ Hate Crime"
                st.write("🛑 You experienced a **Gender and LGBTQ+ Hate Crime**.")
    
    # Display options for further assistance
    if hate_crime_type:
        st.markdown("### How can I assist you further?")
        option = st.selectbox(
            "Choose one of the options below for more information:",
            ("Select...", "Understanding Rights", "Steps to Report a Hate Crime in Berlin", "Local Resources in Berlin", "General Information")
        )
        
        # Retrieve information based on the selected option
        if option != "Select...":
            if option == "Understanding Rights":
                relevant_info = get_relevant_info_with_metadata("What rights do victims of hate crimes have in Germany?")
                st.markdown(f"### Understanding Your Rights\n{relevant_info}")
            
            elif option == "Steps to Report a Hate Crime in Berlin":
                relevant_info = get_relevant_info_with_metadata("Steps to report a hate crime in Germany", section_filter="steps")
                st.markdown(f"### Steps to Report a Hate Crime\n{relevant_info}")
            
            elif option == "Local Resources in Berlin":
                relevant_info = get_relevant_info_with_metadata("Resources available in Berlin for hate crime victims")
                st.markdown(f"### Local Resources in Berlin\n{relevant_info}")
            
            elif option == "General Information":
                relevant_info = get_relevant_info_with_metadata("General information about hate crimes")
                st.markdown(f"### General Information\n{relevant_info}")