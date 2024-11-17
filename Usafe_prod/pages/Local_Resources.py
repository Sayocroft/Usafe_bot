import streamlit as st

def display_local_resources():
    # Page Title
    st.title("Local Resources for Victims of Hate Crimes in Germany")
    
    # Introduction
    st.write("""
    Germany offers numerous resources to support victims of hate crimes. Below, you’ll find information on reporting mechanisms, mental health support, legal aid, and organizations that combat hate speech.
    """)

    # Section 1: Reporting Mechanisms
    st.subheader("📄 Reporting Mechanisms")
    st.markdown("""
    - [Online Strafanzeige](https://www.online-strafanzeige.de): Allows individuals to file criminal complaints online, including hate crimes. Managed by local police authorities with contact details varying by state.
    - [Meldestelle Respect!](https://www.meldestelle-respect.de): Platform to report hate speech and receive expert analysis.
    - [Federal Anti-Discrimination Agency](https://www.antidiskriminierungsstelle.de): Provides counseling and support for those facing discrimination, including hate crimes.
    """)

    # Section 2: Mental Health and Coping Strategies
    st.subheader("🧠 Mental Health and Coping Strategies")
    st.markdown("""
    - [You Are Not Alone](https://www.youarenotalone.ai): Offers tips and resources to help cope with the impact of hate crimes.
    """)

    # Section 3: Legal Aid and Financial Assistance
    st.subheader("⚖️ Legal Aid and Financial Assistance")
    st.markdown("""
    - [HateAid](https://www.hateaid.org): Provides financial support for legal proceedings related to digital violence and hate crimes.
    """)

    # Section 4: Organizations Against Hate Speech
    st.subheader("🛡️ Organizations Against Hate Speech")
    st.markdown("""
    - [Kompetenznetzwerk Hass im Netz](https://www.kompetenznetzwerk-hass-im-netz.de): Dedicated to combating hate speech through various initiatives.
    - [Neue deutsche Medienmacher*innen](https://www.neuemedienmacher.de): Promotes diversity in media to counter hate speech.
    - [Gesellschaft für Freiheitsrechte – Marie Munk Initiative](https://www.freiheitsrechte.org): Protects democracy by addressing hate speech through legal channels.
    - [Ich Bin Hier e.V.](https://www.ichbinhier.eu): Empowers individuals to combat online hate speech.
    """)

    # Section 5: Religion-Based Hate Crime Resources
    st.subheader("✝️ Religion-Based Hate Crime Resources")
    st.markdown("""
    - [Get The Trolls Out!](https://www.getthetrollsout.org): Addresses hate speech related to religion through media monitoring and campaigns.
    """)

    # Section 6: Local Support Resources for Victims in Berlin
    st.subheader("🏙️ Local Support Resources for Victims in Berlin")
    st.markdown("""
    - [Berlin Police – Hate Crime Prevention Unit](https://www.berlin.de): Offers information and support.
    - [Roots Berlin](https://www.rootsberlin.com): Provides counseling for victims of discrimination.
    - [KOP – Campaign for Victims of Police Violence](https://www.kop-berlin.de): Supports individuals affected by police violence and hate crimes.
    - [Verband der Beratungsstellen für Betroffene rechter, rassistischer und antisemitischer Gewalt (VBRG)](https://www.verband-brg.de): Offers counseling, legal assistance, and advocacy.
    """)

    # Section 7: LGBTQ+ and Minority Support Organizations
    st.subheader("🏳️‍🌈 LGBTQ+ and Minority Support Organizations")
    st.markdown("""
    - [GLADT e.V.](https://www.gladt.de): Supports Black and People of Color (LGBTQ+) in Berlin.
    - [Hydra e.V.](https://www.hydra-berlin.de): Offers support for sex workers in Berlin facing violence or discrimination.
    - [LesMigraS](https://www.lesmigras.de): Provides counseling for lesbian, bisexual women, and trans* individuals facing discrimination.
    """)

    # Section 8: Anti-Discrimination Networks
    st.subheader("🚫 Anti-Discrimination Networks")
    st.markdown("""
    - [Antidiskriminierungsverband Deutschland (advd)](https://www.antidiskriminierung.org): A network of anti-discrimination offices that offers counseling and advocacy.
    """)

# Execute the function to display content
if __name__ == "__main__":
    display_local_resources()