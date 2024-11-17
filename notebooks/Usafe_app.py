import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

# Load environment variables
load_dotenv()

# Define the hate crimes types
HATE_CRIMES_TYPE = {
    'anti_religious_def.pdf': 'Anti-religious Hate Crime',
    'racist_def.pdf': 'Racist and Xenophobic Hate Crime',
    'gender_lgbt_def.pdf': 'Gender and LGBTQ+ Hate Crime'
}

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

# Set up the Streamlit title and description
st.title(":safety_vest: Usafe - Your Anti-Discrimination Helpdesk")
st.write("Facing discrimination or hate? Get confidential support and essential guidance in seconds. Your safety and mental health matter.")

# Initialize session state for tracking form submissions
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# Step 1: Define the user form for input
with st.form(key="user_form"):
    user_input = st.text_input("Describe briefly what happened to you:", placeholder="Type here...", key="user_input")
    submit_button = st.form_submit_button(label="Submit")

# Function to retrieve documents using metadata filtering
def get_relevant_info_with_metadata(query, section_filter=None, k=5):
    """
    Retrieve relevant information with metadata filtering and return full content.
    """
    try:
        # Use metadata filtering if a section_filter is provided
        search_kwargs = {'k': k}
        if section_filter:
            search_kwargs['metadata_filter'] = {"section": section_filter}
        
        # Retrieve multiple relevant documents
        results = retriever_general.get_relevant_documents(query, search_kwargs=search_kwargs)
        
        if results:
            # Combine content from all retrieved documents
            full_content = " ".join([result.page_content.strip() for result in results if result.page_content])
            
            # DEBUG: Print the full content retrieved
            st.write(f"Retrieved content: {full_content}")
            
            return full_content if full_content else "No information available at the moment."
        
        return "No information found for the given query."
    except AttributeError as e:
        st.error(f"Error during retrieval: {e}")
        return "An error occurred while retrieving the information."

# Step 5: Handle form submission
if submit_button:
    st.session_state['submitted'] = True

# Step 6: Check if the input was submitted and handle user interaction
if st.session_state['submitted'] and st.session_state['user_input']:
    st.markdown("### I’m truly sorry that you’ve gone through this.")
    st.markdown("No one should ever face such treatment. Thank you for trusting me with your story.")

    # Step 7: Retrieve relevant documents from the combined vector store to identify hate crime type
    combined_results = retriever_combined.get_relevant_documents(st.session_state['user_input'])
    
    # Identify the type of hate crime
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

# Step 8: Show the options dropdown only after the hate crime type is detected
    if hate_crime_type:
        st.markdown("### How can I assist you further?")
        option = st.selectbox(
            "Choose one of the options below for more information:",
            ("Select...", "Understanding Rights", "Steps to Report a Hate Crime in Berlin", "Local Resources in Berlin", "General Information")
        )
        
        # Retrieve information based on the selected option
        if option != "Select...":
            if option == "Understanding Rights":
                option_query = "What rights do victims of hate crimes have in Germany?"
                relevant_info = get_relevant_info_with_metadata(option_query)
                st.markdown(f"### Understanding Your Rights\n{relevant_info if relevant_info else 'No information available at the moment.'}")
            
            elif option == "Steps to Report a Hate Crime in Berlin":
                 option_query = "Please provide a detailed step-by-step guide on reporting a hate crime in Germany, specifically Document the Incident, Preserve Evidence, Prepare language barrier, Visit the police station, report crime online, seek additional support."
                 relevant_info = get_relevant_info_with_metadata(option_query, section_filter="steps")
                 st.markdown(f"### Steps to Report a Hate Crime\n{relevant_info if relevant_info else 'No information available at the moment.'}")
            
            elif option == "Local Resources in Berlin":
                option_query = "What resources are available in Berlin for hate crime victims?"
                relevant_info = get_relevant_info_with_metadata(option_query)
                st.markdown(f"### Local Resources in Berlin\n{relevant_info if relevant_info else 'No information available at the moment.'}")
            
            elif option == "General Information":
                option_query = "Provide general information about hate crimes."
                relevant_info = get_relevant_info_with_metadata(option_query)
                st.markdown(f"### General Information\n{relevant_info if relevant_info else 'No information available at the moment.'}")