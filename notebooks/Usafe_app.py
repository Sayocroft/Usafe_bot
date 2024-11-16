import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

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
def get_relevant_info_with_metadata(query, metadata_filter=None, k=2, max_sentences=3):
    """
    Retrieve a concise response using metadata filters.
    """
    try:
        if metadata_filter:
            results = retriever_general.get_relevant_documents(
                query,
                search_kwargs={'k': k, 'metadata_filters': metadata_filter}
            )
        else:
            results = retriever_general.get_relevant_documents(query, search_kwargs={'k': k})

        if results:
            content = results[0].page_content.strip()
            # Limit to the first few sentences
            sentences = content.split('. ')
            return '. '.join(sentences[:max_sentences]) + '.' if len(sentences) > max_sentences else content
        else:
            return None
    except AttributeError as e:
        st.error(f"Error during retrieval: {e}")
        return None
    

def get_combined_response(query, k=2, max_sentences=3):
    """
    Retrieve relevant documents from the vector store and generate an LLM response.
    """
    # Step 1: Retrieve relevant documents from the combined vector store
    combined_results = retriever_combined.get_relevant_documents(query, search_kwargs={'k': k})
    
    # Step 2: Extract content if documents are found
    retrieved_content = ""
    if combined_results:
        retrieved_content = combined_results[0].page_content.strip()
        sentences = retrieved_content.split('. ')
        retrieved_content = '. '.join(sentences[:max_sentences]) + '.' if len(sentences) > max_sentences else retrieved_content
    
    # Step 3: Use the LLM to generate a response if needed
    try:
        if retrieved_content:
            # Pass the content as a conversation to the generate method
            llm_response = llm.generate(
                messages=[
                    {"role": "system", "content": "You are an expert on hate crimes and support resources."},
                    {"role": "user", "content": f"Based on the following information: {retrieved_content}. Answer the user query: {query}"}
                ]
            )
        else:
            llm_response = llm.generate(
                messages=[
                    {"role": "system", "content": "You are an expert on hate crimes and support resources."},
                    {"role": "user", "content": f"Please help answer the following query: {query}"}
                ]
            )
        # Extracting the response content
        return llm_response.content if llm_response else "No response generated."
    except Exception as e:
        st.error(f"Error with LLM: {e}")
        return "I'm sorry, I couldn't process your request at the moment."

# Example usage within Streamlit
if st.session_state['submitted'] and st.session_state['user_input']:
    user_query = st.session_state['user_input']
    response = get_combined_response(user_query)
    st.write(response)
    
# Function to display results in a formatted way
def display_results(results, header):
    """Display retrieved documents in a user-friendly format."""
    if results and results[0]:
        st.markdown(f"### {header}")
        content = results[0]
        st.write(f"{content}")
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
        definition = get_relevant_info_with_metadata(
            query=definition_query,
            metadata_filter={"source": "definitions"},
            k=2
        )
    else:
        definition_query = f"Definition related to {st.session_state['user_input']}"
        definition = get_relevant_info_with_metadata(
            query=definition_query,
            metadata_filter={"source": "definitions"},
            k=2
        )
    
    # Display the retrieved definition
    if definition:
        st.markdown(f"### What is a Hate Crime\n{definition}")
    else:
        st.write("No definition found.")       

    # Step 9: Retrieve specific German laws related to the identified hate crime
    if hate_crime_type:
        german_law_query = f"Legal protections under German law for {hate_crime_type}"
        law = get_relevant_info_with_metadata(
            query=german_law_query,
            metadata_filter={"source": "laws"},
            k=2
        )
    else:
        german_law_query = f"German laws protecting against {st.session_state['user_input']}"
        law = get_relevant_info_with_metadata(
            query=german_law_query,
            metadata_filter={"source": "laws"},
            k=2
        )
    
    # Display the retrieved legal information
    if law:
        st.markdown(f"### What laws in Germany protect you\n{law}")
    else:
        st.write("No definition found.")

    # Step 10: Provide additional options for users
    option = st.selectbox(
        "Choose one of the options below for more information:",
        ("Select...", "Understanding Rights", "Steps to Report a Hate Crime in Berlin", "Local Resources in Berlin", "General Information")
    )
    
    # Handle user selection and retrieve specific information
    if option != "Select...":
        if option == "Understanding Rights":
            rights_info = get_relevant_info_with_metadata(
                query="The German Criminal Code includes several sections addressing hate crimes",
                metadata_filter={"source": "laws"},
                k=2
            )
            display_results([rights_info], "Understanding Your Rights")
        
        elif option == "Steps to Report a Hate Crime in Berlin":
            report_info = get_relevant_info_with_metadata(
                query="To report a hate crime, document the incident, gather evidence, prepare for language barriers, contact local law enforcement, and reach out to support organizations.",
                metadata_filter={"source": "reporting_steps"},
                k=2
            )
            display_results([report_info], "Steps to Report a Hate Crime")
        
        elif option == "Local Resources in Berlin":
            resources_info = get_relevant_info_with_metadata(
                query="Resources in Berlin for hate crime victims",
                metadata_filter={"source": "resources"},
                k=2
            )
            display_results([resources_info], "Local Resources in Berlin")
        
        elif option == "General Information":
            general_info = get_relevant_info_with_metadata(
                query="General information about hate crimes",
                metadata_filter={"source": "history"},
                k=2
            )
            display_results([general_info], "General Information")
    

