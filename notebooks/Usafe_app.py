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
def get_relevant_info_with_metadata(query, metadata_filter=None):
    """
    Retrieve documents using metadata filters.
    """
    try:
        if metadata_filter:
            results = retriever_general.get_relevant_documents(
                query,
                search_kwargs={'k': 5, 'metadata_filters': metadata_filter}
            )
        else:
            results = retriever_general.get_relevant_documents(query, search_kwargs={'k': 5})
        
        # Return the results without printing any debug information
        return results
    except AttributeError as e:
        st.error(f"Error during retrieval: {e}")
        return None

# Function to display results in a formatted way
def display_results(results, header):
    """Display retrieved documents in a user-friendly format."""
    if results:
        st.markdown(f"### {header}")
        for result in results:
            # Display only the content, without metadata or file paths
            content = result.page_content.strip()
            st.write(f"- {content}")
    else:
        st.write("No relevant information found.")

# Step 5: Handle form submission
if submit_button:
    st.session_state['submitted'] = True

# Step 6: Check if the input was submitted and handle user interaction
if st.session_state['submitted'] and st.session_state['user_input']:
    st.markdown("### I’m truly sorry that you’ve gone through this.")
    st.markdown("No one should ever face such treatment. Thank you for trusting me with your story.")

    # Step 7: Retrieve relevant documents from the combined vector store to identify hate crime type
    combined_results = retriever_combined.get_relevant_documents(st.session_state['user_input'])
    
    # Identify the type of hate crime based on the combined results
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

    # Step 8: Retrieve a quick definition of the identified hate crime type
    if hate_crime_type:
        definition_query = f"Definition of {hate_crime_type}"
        definition_results = get_relevant_info_with_metadata(
            query=definition_query,
            metadata_filter={"source": "definitions"}
        )
    else:
        definition_query = f"Definition related to {st.session_state['user_input']}"
        definition_results = get_relevant_info_with_metadata(
            query=definition_query,
            metadata_filter={"source": "definitions"}
        )
    
    # Display the retrieved definition
    display_results(definition_results, "Definition of the Hate Crime")

    # Step 9: Retrieve specific German laws related to the identified hate crime
    if hate_crime_type:
        german_law_query = f"Legal protections under German law for {hate_crime_type}"
        law_results = get_relevant_info_with_metadata(
            query=german_law_query,
            metadata_filter={"source": "laws"}
        )
    else:
        german_law_query = f"German laws protecting against {st.session_state['user_input']}"
        law_results = get_relevant_info_with_metadata(
            query=german_law_query,
            metadata_filter={"source": "laws"}
        )
    
    # Display the retrieved legal information
    display_results(law_results, "How German Law Protects You")

    # Step 5: Provide additional options for users
    option = st.selectbox(
        "Choose one of the options below for more information:",
        ("Select...", "Understanding Rights", "Steps to Report a Hate Crime in Berlin", "Local Resources in Berlin", "General Information")
    )
    
    # Handle user selection and retrieve specific information
    if option != "Select...":
        if option == "Understanding Rights":
            rights_info = get_relevant_info_with_metadata("rights", metadata_filter={"source": "definitions"})
            display_results(rights_info, "Understanding Your Rights")
        elif option == "Steps to Report a Hate Crime in Berlin":
            report_info = get_relevant_info_with_metadata("report", metadata_filter={"source": "reporting_steps"})
            display_results(report_info, "Steps to Report a Hate Crime")
        elif option == "Local Resources in Berlin":
            resources_info = get_relevant_info_with_metadata("resources", metadata_filter={"source": "resources"})
            display_results(resources_info, "Local Resources in Berlin")
        elif option == "General Information":
            general_info = get_relevant_info_with_metadata("general info", metadata_filter={"source": "history"})
            display_results(general_info, "General Information")

