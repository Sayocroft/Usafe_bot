import streamlit as st

def display_understanding_rights():
    # Page Title
    st.title("Understanding Your Rights in Germany")

    # Display the main content
    st.write("""
    **Import** : In Germany, hate crimes are not defined as a separate offense. 
    
    Germany’s approach is a blend of legal enforcement, constitutional guarantees, international cooperation, and grassroots efforts, all aimed at protecting vulnerable communities and promoting an inclusive society.
  
    """)

    # Section on the German Criminal Code
    st.header("Key Sections of the German Criminal Code You Should be Aware of")
    st.write("""
    - **Section 46 StGB**: Allows courts to consider discriminatory motives during sentencing, enhancing penalties for bias-motivated crimes.
             
    - **Section 130 StGB (Volksverhetzung)**: Specifically targets incitement to hatred, hate speech, and acts intended to incite violence against racial, religious, and national communities.
             
    - **Section 166 StGB**: Criminalizes public defamation of religious groups if it threatens public peace.
             
    - **The Basic Law (Grundgesetz, GG)**:
        - **Article 4**: Ensures freedom of religion.
        - **Article 3**: Prohibits discrimination based on race, ethnicity, or religion.
             

                     
    - **International Convention on the Elimination of All Forms of Racial Discrimination (ICERD)**: Reinforces Germany’s anti-racist measures.
    """)

# Execute the function to display content
if __name__ == "__main__":
    display_understanding_rights()