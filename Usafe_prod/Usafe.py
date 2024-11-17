import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load environment variables
load_dotenv()

# Define hate crime types mapping
HATE_CRIMES_TYPE = {
    'anti_religious_def.pdf': 'Anti-religious Hate Crime',
    'racist_def.pdf': 'Racist and Xenophobic Hate Crime',
    'gender_lgbt_def.pdf': 'Gender and LGBTQ+ Hate Crime'
}

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Usafe",
    page_icon=":safety_vest:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
    vector_store = FAISS.load_local(
        folder_path=path, 
        embeddings=embedding_model, 
        allow_dangerous_deserialization=True
    )
    return vector_store.as_retriever()

# Load both vector stores
retriever_combined = load_vector_store('notebooks/vector_databases/usafe_combined')
retriever_general = load_vector_store('notebooks/vector_databases/usafe_general')

# Step 3: Set up VADER Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(user_input):
    """Analyze the sentiment using VADER."""
    sentiment_scores = analyzer.polarity_scores(user_input)
    if sentiment_scores['compound'] <= -0.3:
        return "negative"
    elif sentiment_scores['compound'] >= 0.3:
        return "positive"
    else:
        return "neutral"

# Set up the Streamlit title and description
st.title(":safety_vest: Usafe - Your Anti-Discrimination Helpdesk")
st.write("Facing discrimination or hate? Get confidential support and essential guidance in seconds. Your safety and mental health matter.")

# Initialize session state for tracking form submissions
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# Step 4: Define the user form for input
with st.form(key="user_form"):
    user_input = st.text_input("Describe briefly what happened to you:", placeholder="Type here...", key="user_input")
    submit_button = st.form_submit_button(label="Submit")

# Function to retrieve documents using metadata filtering
def get_relevant_info_by_option(query, section_filter=None, k=5):
    """Retrieve relevant information based on metadata filtering using the general vector store."""
    try:
        search_kwargs = {'k': k}
        if section_filter:
            search_kwargs['metadata_filter'] = {"section": section_filter}
        results = retriever_general.get_relevant_documents(query, search_kwargs=search_kwargs)
        if results:
            return " ".join([doc.page_content.strip() for doc in results if doc.page_content]) or "No information available."
        return "No information found for the selected option."
    except Exception as e:
        st.error(f"Error retrieving information: {e}")
        return "An error occurred while retrieving information."

# Step 5: Handle form submission
if submit_button:
    st.session_state['submitted'] = True

# Run the following only if the form is submitted
if st.session_state.get('submitted'):

# Step 5.2: Retrieve relevant documents to identify hate crime type
    combined_results = retriever_combined.get_relevant_documents(st.session_state['user_input'])
    
    hate_crime_type = None
    if combined_results:
        hate_crime_source = combined_results[0].metadata.get('source')
        if hate_crime_source:
            if "anti_religious_def.pdf" in hate_crime_source:
                hate_crime_type = "Anti-Religious Hate Crime"
                st.write("### **Unfortunately, you experienced an Anti-Religious Hate Crime**")
            elif "racist_def.pdf" in hate_crime_source:
                hate_crime_type = "Racist and Xenophobic Hate Crime"
                st.write("### **Unfortunately, you experienced a Racist and Xenophobic Hate Crime**")
            elif "gender_lgbt_def.pdf" in hate_crime_source:
                hate_crime_type = "Gender and LGBTQ+ Hate Crime"
                st.write("### **Unfortunately, you have experienced a Gender and Anti-LGBTQ+ Hate Crime**")


    # Step 5.1: Analyze the sentiment of the user's input
    sentiment = analyze_sentiment(st.session_state['user_input'])

    if sentiment == "negative":
        st.write("""
        🛑 **I sense that you’re feeling distressed**, and I want you to know you’re not alone. Your feelings are valid, and it's okay to take a moment to breathe.  
        - **Prioritize your safety**: If you're in immediate danger, please call the Berlin police at **110** or reach out to someone nearby for help.
        - **Reach out for support**: You don’t have to go through this alone. Connecting with a friend, family member, or support hotline can make a difference.
        - **Resources**: Below, you’ll find links to organizations and support groups that can provide assistance. Remember, it’s okay to seek help.
        """)
        st.warning("⚠️ Your safety and mental well-being are important. Take your time, and let’s find the best resources to support you.")

    elif sentiment == "positive":
        st.write("""
        🟢 **I'm glad to hear you're feeling okay!** It's great that you're in a positive headspace.
        - Let's focus on the next steps to ensure you have all the information and support you need.
        - Feel free to explore the resources or ask about anything specific you'd like assistance with.
        """)
        st.success("😊 Thank you for reaching out. Let's find the information that can help you further.")

    else:  # Neutral sentiment
        st.write("""
        🟡 **I’m truly sorry you had to go through that**. Thank you for trusting me enough to reach out.
        - Please take a moment to review the resources that might be helpful for your situation.
        - If you’re unsure where to start, you can explore options like understanding your rights, how to report an incident, or connecting with support organizations.
        """)
        st.info("🔍 Let’s proceed to gather more information and guide you towards the best support available.")
        
 
# Conditionally display the sidebar content only after form submission
if st.session_state.get('submitted'):
    with st.sidebar:
        st.success("Your Anti-Discrimination Helpdesk")
    
# Add an expandable section for practical information
with st.expander("### Before I can provide more practical information..."):
    st.markdown("""
    🛑 **Prioritize Your Safety** 
       - Move to a safe place if you feel threatened. If needed, call emergency services or ask someone nearby for assistance.
    
    📞 **Reach Out for Support**  
       - Connect with a trusted friend, family member, or support organization. Talking to someone can help you feel grounded.
    
    📝 **Document the Incident** 
       - Write down details of the incident, such as the date, time, location, and any witnesses.
    
    💛 **Focus on Your Well-being**   
       - Take the time you need to heal. Speak to a counselor, engage in activities you enjoy, or rest. Your well-being matters.
    """)