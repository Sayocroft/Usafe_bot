# Step 4: Display results from the appropriate vector store
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



if query:
    st.write("Searching in the general knowledge base...")
    general_response = retriever_general.get_relevant_documents(query)
    
    st.write("Searching in the specific hate crime database...")
    combined_response = retriever_combined.get_relevant_documents(query)
    
    # Display results from the general vector store
    st.subheader("General Information")
    for i, doc in enumerate(general_response):
        st.write(f"{i + 1}. {doc.page_content}")

    # Display results from the combined vector store
    st.subheader("Specific Hate Crime Information")
    for i, doc in enumerate(combined_response):
        st.write(f"{i + 1}. {doc.page_content}")




        if st.button("Submit"):
    if user_input:
        # Step 1: Detect the hate crime type using `invoke()`
        try:
            # Retrieve the response from the combined vector store
            hate_crime_response = retriever_combined.invoke(
                {"input": f"Please classify the following incident description to detect the hate crime type:\n'{user_input}'"}
            )

            # Debug: Print the raw response to understand its structure
            st.write("Raw Response:", hate_crime_response)

            # Extract the detected hate crime type from the response
            detected_hate_crime = hate_crime_response.get('result', {}).get('content', "Unknown")
            st.write(f"Detected Hate Crime: {detected_hate_crime}")

            # Provide an empathetic response
            st.write("I'm really sorry to hear about your experience. You are not alone, and we're here to help you find justice and support.")

        except Exception as e:
            st.error(f"Error in detecting hate crime: {e}")

        # Step 2: Offer guidance options
        st.write("Please choose one of the following options to proceed:")
        options = ["Understand Your Rights", "Report a Crime", "Find Local Resources", "General Information"]
        selected_option = st.radio("Select an option", options)

        if selected_option:
            query_map = {
                "Understand Your Rights": "laws",
                "Report a Crime": "reporting_steps",
                "Find Local Resources": "resources",
                "General Information": "history"
            }
            query_type = query_map[selected_option]

            try:
                # Retrieve information from the general vector store
                general_response = retriever_general.invoke(
                    {"input": f"Please provide information about {query_type} related to hate crimes."}
                )

                # Debug: Print the raw response to understand its structure
                st.write("Raw Response:", general_response)

                # Extract the answer from the response
                response_text = general_response.get('result', {}).get('content', "No information found.")
                st.write(response_text)

            except Exception as e:
                st.error(f"Error retrieving information: {e}")