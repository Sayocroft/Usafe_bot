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

# Define the hate crimes types
HATE_CRIMES_TYPE = {
    'anti_religious_def.pdf': 'Anti-religious Hate Crime',
    'racist_def.pdf': 'Racist and Xenophobic Hate Crime',
    'gender_lgbt_def.pdf': 'Gender and LGBTQ+ Hate Crime'
}

def detect_hate_crime_type(inquiry, retrieval_chain=retriever_combined):
    """
    Detects the type of hate crime based on user input and displays the result in Streamlit.
    """
    try:
        # Query the retrieval chain with the user inquiry
        result = retrieval_chain.invoke({"input": inquiry})
        
        # Check if the response contains context information
        if result and 'context' in result and result['context']:
            # Extract the source from the metadata
            metadata_source = result['context'][0].dict().get('metadata', {}).get('source', "")
            
            # Detect the hate crime type using the HATE_CRIMES_TYPE mapping
            detected_type = HATE_CRIMES_TYPE.get(metadata_source.split('/')[-1], "Unknown")
        else:
            detected_type = "Unknown"

        # Display the detected type using Streamlit
        st.write(f"**Detected Hate Crime Type:** {detected_type}")
        return detected_type

    except Exception as e:
        st.error(f"Error detecting hate crime type: {e}")
        return "Unknown"

def handle_user_query(inquiry):
    """
    Handles user query by detecting hate crime type and offering options using Streamlit.
    """
    # Step 1: Detect the hate crime type
    detected_type = detect_hate_crime_type(inquiry)
    st.write(f"**Detected Hate Crime Type:** {detected_type}")

    # Step 2: Present user options using Streamlit
    st.write("What information would you like to access?")
    option = st.selectbox(
        "Choose an option:",
        ["Select an option", "Relevant Laws Germany", "Local Resources and Support", 
         "Steps to Report a Crime in Germany", "Generic Information"]
    )

    # Step 3: Determine the query based on user selection
    pdf_query = ""
    if option == "Relevant Laws Germany":
        pdf_query = "Relevant laws related to hate crimes in Germany"
    elif option == "Local Resources and Support":
        pdf_query = "Local resources: NGOs, Legal Aid, Counseling, etc., to support hate crime victims"
    elif option == "Steps to Report a Crime in Germany":
        pdf_query = "Steps on how to report a hate crime in Germany"
    elif option == "Generic Information":
        pdf_query = "General information on hate crimes, psychological effects, and resources"
    
    # If no valid option is selected
    if not pdf_query:
        st.warning("Please select a valid option.")
        return

    # Step 4: Retrieve and display the response from the vector store
    response = retriever_general.invoke({"input": pdf_query})
    
    # Check if the response contains an answer
    answer = response.get('answer', 'No relevant information found').strip("\n")
    st.write("**Response:**")
    st.write(answer)

# Example usage within Streamlit
st.title("Usafe ChatBot")
user_input = st.text_input("Enter your inquiry:")
if user_input:
    handle_user_query(user_input)
  

# Add a button to trigger the query
if st.button("Submit"):
    if user_input:
        handle_user_query(user_input)
    else:
        st.warning("Please enter a description of the incident.")






