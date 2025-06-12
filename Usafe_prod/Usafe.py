import os
from dotenv import load_dotenv
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load environment variables
load_dotenv()

# Define hate crime types mapping
HATE_CRIMES_TYPE = {
    'anti_religious_def.pdf': 'Anti-religious Hate Crime',
    'racist_def.pdf': 'Racist and Xenophobic Hate Crime',
    'gender_lgbt_def.pdf': 'Gender and LGBTQI+ Hate Crime'
}


# Set page configuration
st.set_page_config(
    page_title="Usafe",
    page_icon=":safety_vest:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Display the main title and subtitle with increased font size
st.markdown("""
    <h1 style='text-align: center; font-size: 5rem;'>
        🦺 Usafe
    </h1>
    <h2 style='text-align: center; color: #666; font-size: 2.5rem;'>
        Your Anti-Hate Crime Helpdesk
    </h2>
""", unsafe_allow_html=True)

# Display the introductory message with moderate size and subtle emphasis
st.markdown("""
    <p style='text-align: center; font-size: 1.2rem; font-weight: 600;'>
        Get confidential support and essential guidance in seconds. 
    </p>
""", unsafe_allow_html=True)


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

# Step 3: Set up VADER Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(user_input):
    """Classify sentiment as either negative or neutral using VADER."""
    sentiment_scores = analyzer.polarity_scores(user_input)
    compound_score = sentiment_scores['compound']
    negative_score = sentiment_scores['neg']

    # Enhanced classification logic:
    # - Classify as "negative" if the compound score is below -0.2 or the negative score is above 0.3
    if compound_score <= -0.2 or negative_score > 0.3:
        return "negative"
    else:
        return "neutral"

# Initialize session state for tracking form submissions
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# Step 4: Define the user form for input
with st.form(key="user_form"):
    user_input = st.text_area(
        "",  # No label
        placeholder="Describe briefly what happened to you...",
        key="user_input",
        height=85  # Adjust height for better user experience
    )

    submit_button = st.form_submit_button(
        label="⚖️ Submit",  # Add an emoji to make the button more inviting
        help="Click here to submit your information."  # Tooltip for extra guidance
    )
    
    # Display personalized information based on the detected hate crime type
def display_practical_info(hate_crime_type):
    """
    Display practical information within an expandable section based on the detected hate crime type.
    """
    with st.expander("### If you’re unsure where to begin, you can start by exploring topics like..."):
        if hate_crime_type == "Gender and LGBTQI+ Hate Crime":
            st.write("### Top 3 Essential Steps")
            st.markdown("""
            - **Law**: In Germany, discrimination based on gender identity is illegal. You have rights under the General Equal Treatment Act (AGG).
            - **Support Organization**: Contact **LesMigraS** for counselling.
            - **Legal Aid**: Visit **HateAid** for free legal support.
            """)
        elif hate_crime_type == "Racist and Xenophobic Hate Crime":
            st.write("### Top 3 Essential Steps")
            st.markdown("""
            - **Law**: In Germany, hate crimes based on race and ethnicity are punishable under the Criminal Code.
            - **Support Organization**: Reach out to **ReachOut Berlin** for assistance with racism-related incidents.
            - **Legal Aid**: Contact **VBRG** for support and legal guidance.
            """)
        elif hate_crime_type == "Anti-Religious Hate Crime":
            st.write("### Resources for Anti-Religious Hate Crime")
            st.markdown("""
            - **Law**: Anti-religious discrimination is prohibited under the Basic Law for the Federal Republic of Germany.
            - **Support Organization**: Contact **Berlin Interfaith Council** for community support.
            - **Legal Aid**: Get in touch with **European Center for Law and Justice** for legal help.
            """)


# Step 5: Handle form submission
if submit_button:
    st.session_state['submitted'] = True

# Run the following only if the form is submitted
if st.session_state.get('submitted'):

    # Step 5.1: Analyze the sentiment of the user's input
    sentiment = analyze_sentiment_vader(st.session_state['user_input'])

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
                hate_crime_type = "Gender and LGBTQI+ Hate Crime"
                st.write("### **Unfortunately, you have experienced a Gender and Anti-LGBTQI+ Hate Crime**")
    
    # Step 5.3: Display the sentiment-based message
    if sentiment == "negative":
        st.write("""
        **I’m really sorry you had to go through this**, and I want you to know you’re not alone. It’s okay to take a moment to breathe and gather yourself.  
        - **Prioritize your safety**: If you’re in immediate danger, please don’t hesitate to call the Berlin police at **110** or reach out to someone nearby who can assist you.
        - **Reach out for support**: You don’t have to face this alone. Speaking with a trusted friend, family member, or support organization can make a big difference. Remember, there are people who care deeply and are ready to help.
        """)
        st.warning("⚠️ **Check the sidebar** for detailed information and links to organizations that can provide practical support. Let’s find the best resources to support you.")

    elif sentiment == "neutral":
        st.write("""
        🟡 **I’m truly sorry you had to go through that**. Thank you for trusting me enough to reach out.
        - **Review Resources**: Please take a moment to review the resources that might be helpful for your situation.
        - **Check the sidebar**: If you’re unsure where to start, you can explore options like understanding your rights, how to report an incident, or connecting with support organizations.
        """)
        st.info("🔍 Let’s proceed to gather more information and guide you towards the best support available.")

    # Display practical information based on the detected hate crime type
    if hate_crime_type:
        display_practical_info(hate_crime_type)
    