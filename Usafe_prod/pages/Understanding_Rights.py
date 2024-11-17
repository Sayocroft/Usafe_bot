import streamlit as st

def display_understanding_rights():
    # Page Title
    st.title("Understanding Your Rights in Germany")

    # Display the introductory content
    st.write("""
    In Germany, there are specific laws and legal provisions aimed at protecting individuals from hate crimes based on their gender, sexual orientation, religion, or race. Here’s an overview of the key legal protections for each type of hate crime:
    """)

    # Section on Gender/LGBTQI+ Hate Crime
    st.header("1. Gender / LGBTQI+ Hate Crime")
    st.write("""
    - **Basic Law (Grundgesetz) - Article 3**: Protects against discrimination on the basis of gender and sexual orientation. It guarantees equality before the law and prohibits discrimination based on sex, parentage, race, language, homeland and origin, faith, religious or political opinions, or disability.
    - **Criminal Code (Strafgesetzbuch, StGB)**:
        - **Section 130 (Incitement to Hatred)**: Criminalizes incitement to hatred or violence against a group, including those based on sexual orientation and gender identity.
        - **Section 185 (Insult)** & **Section 186 (Defamation)**: Protects individuals from derogatory or slanderous statements made because of their sexual orientation or gender.
        - **Section 46(2) (Sentencing Guidelines)**: Recognizes hate-motivated crimes as an aggravating factor, allowing harsher sentences for offenses committed out of prejudice against LGBTQI+ individuals.
    """)

    # Section on Anti-Religious Hate Crime
    st.header("2. Anti-Religious Hate Crime")
    st.write("""
    - **Basic Law (Grundgesetz) - Article 4**: Guarantees freedom of religion and belief, protecting individuals’ right to practice their religion without discrimination.
    - **Criminal Code (Strafgesetzbuch, StGB)**:
        - **Section 166 (Defamation of Religions)**: Prohibits defamation of religious communities if it is likely to disturb public peace.
        - **Section 130 (Incitement to Hatred)**: Criminalizes incitement to hatred or violence against religious groups.
        - **Section 167 (Disruption of Religious Services)**: Criminalizes disruptions or desecrations of religious ceremonies or places of worship.
    """)

    # Section on Racist and Xenophobic Hate Crime
    st.header("3. Racist and Xenophobic Hate Crime")
    st.write("""
    - **Basic Law (Grundgesetz) - Article 3**: Ensures equality and prohibits discrimination based on race, ethnic origin, or heritage.
    - **Criminal Code (Strafgesetzbuch, StGB)**:
        - **Section 130 (Incitement to Hatred)**: Specifically targets incitement to hatred or violence against people based on race, ethnicity, or national origin.
        - **Section 86a (Use of Symbols of Unconstitutional Organizations)**: Criminalizes the use of symbols associated with racism, neo-Nazism, or xenophobic ideologies.
        - **Section 46(2) (Sentencing Guidelines)**: Allows for harsher sentences for crimes motivated by racial or ethnic prejudice.
    """)

    # Section on Additional Protections
    st.header("Additional Protections")
    st.write("""
    - **General Equal Treatment Act (Allgemeines Gleichbehandlungsgesetz, AGG)**: Aims to prevent discrimination in employment, education, and access to goods and services based on race, gender, religion, or sexual orientation.
    - **Victims’ Rights Reform Act (Opferschutzgesetz)**: Strengthens the rights of victims of hate crimes, offering support services and legal protections.

    These laws demonstrate Germany’s commitment to protecting individuals from hate crimes based on gender, sexual orientation, religion, or race. The Criminal Code is frequently applied in conjunction with other protective measures to ensure that victims receive justice and that offenders are held accountable.
    """)

# Execute the function to display content
if __name__ == "__main__":
    display_understanding_rights()