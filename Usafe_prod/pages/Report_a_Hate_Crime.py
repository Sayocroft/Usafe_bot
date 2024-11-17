import streamlit as st

def display_reporting_steps():
    # Page Title
    st.title("Steps to Report a Hate Crime in Germany")

    # Introduction
    st.write("""
    If you or someone you know has experienced a hate crime, it's essential to take action. 
    Here are the steps to report the incident and seek support in Germany.
    """)

    # Step 1: Document the Incident
    st.header("1. Document the Incident")
    st.write("""
    Gather information about the event, including photos, videos, witness statements, and detailed descriptions of what happened 
    (time, location, and identifying features of the perpetrator).
    """)

    # Step 2: Preserve Digital Evidence
    st.header("2. Preserve Digital Evidence")
    st.write("""
    Save any online messages, emails, or social media posts related to the incident. 
    Screenshots are useful if hate speech or threats occurred online.
    """)

    # Step 3: Prepare for Language Barriers
    st.header("3. If you don't speak german...")
    st.write("""
    It may be helpful to bring someone who can assist with translation when reporting the incident at a police station.
    """)

    # Step 4: Visit Your Local Police Station
    st.header("4. Visit Your Local Police Station")
    st.write("""
    Bring all collected documentation and explain the details to the officer, emphasizing that it was a hate crime. 
    Request a case reference number for future follow-ups.
    """)

    # Step 5: Report Online
    st.header("5. Report Online")
    st.write("""
    If unable to visit a police station, you can file a report online via local authorities’ websites, 
    such as the [Berlin Police Online Reporting Portal](https://www.berlin.de/polizei/).
    """)

    # Step 6: Seek Additional Support
    st.header("6. Seek Additional Support")
    st.write("""
    If needed, reach out to organizations for translation support, legal assistance, or mental health counseling.
    """)

# Execute the function to display content
if __name__ == "__main__":
    display_reporting_steps()