import streamlit as st

def display_general_information():
    # Page Title
    st.title("General Information on Hate Crimes")
    
    # Introduction
    st.write("""
    A hate crime (also known as a bias crime) occurs when a perpetrator targets a victim based on their physical appearance or perceived membership in a specific social group. 
    These groups may include race, ethnicity, disability, language, nationality, political views, age, religion, sex, gender identity, or sexual orientation.
    Non-criminal actions motivated by these biases are termed "bias incidents." Examples of hate crimes include physical assault, homicide, property damage, bullying, harassment, 
    verbal abuse, offensive graffiti, or hate mail.
    """)

    # Section 1: History of Hate Crimes
    st.subheader("📜 History of Hate Crimes")
    st.markdown("""
    The term **"hate crime"** gained prominence in the U.S. during the 1980s, although such crimes have existed throughout history:
    - Roman persecution of Christians.
    - Nazi genocide of Jews.
    - European colonial violence against indigenous peoples.
    - In the U.S., lynchings, cross burnings, and attacks on ethnic minorities and LGBTQ+ communities were common.
    - More recently, during the COVID-19 pandemic, there was a surge in anti-Chinese violence, as documented by organizations like the [NEVER AGAIN Association](https://www.nigdywiecej.org) in Poland.
    """)

    # Section 2: Psychological Effects of Hate Crimes
    st.subheader("🧠 Psychological Effects of Hate Crimes")
    st.markdown("""
    Hate crimes have severe psychological impacts on both individuals and communities:
    - Victims may experience trauma, depression, low self-esteem, and symptoms of PTSD.
    - Targeted groups often feel increased fear and vulnerability.
    - Broader communities can become divided, weakening multicultural cohesion.
    - Studies indicate that hate crimes also negatively impact educational and socioeconomic outcomes for affected groups.
    """)

    # Section 3: Motivation Behind Hate Crimes
    st.subheader("🔍 Motivation Behind Hate Crimes")
    st.markdown("""
    Sociologists like Jack McDevitt and Jack Levin identify primary motives behind hate crimes:
    - **Thrill-seeking**: Committed for excitement, often by groups targeting vulnerable individuals.
    - **Defensive motives**: Aimed at protecting one’s community from perceived threats.
    - **Retaliatory motives**: Driven by revenge for perceived offenses.
    - **Mission-oriented crimes**: Ideologically motivated, often targeting symbolically significant sites.
    
    The **Self-Control Theory** offers insights into hate crime motivations, suggesting that social, cultural, and individual factors contribute to these biases. 
    Offenders often develop biases through social interactions and biased media exposure.
    """)

    # Section 4: Risk Management for Hate Crime Offenders
    st.subheader("🛡️ Risk Management for Hate Crime Offenders")
    st.markdown("""
    Research on risk management tools for hate crime offenders is limited, but commonly used tools include:
    - **Violence Risk Appraisal Guide (VRAG)**: Assesses the risk of violent recidivism.
    - **Psychopathy Checklist-Revised (PCL-R)**: Evaluates psychopathic tendencies and recidivism risks.
    """)

# Execute the function to display content
if __name__ == "__main__":
    display_general_information()