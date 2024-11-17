import streamlit as st
import usafe_responses as responses

st.title("Usafe ChatBot")
st.write("Get guidance and support on hate crimes. Let's find the information you need.")

def get_crime_type(user_input):
    user_input = user_input.lower()
    if "racism" in user_input:
        return "racism"
    elif "gender" in user_input:
        return "gender discrimination"
    elif "religion" in user_input:
        return "religious discrimination"
    elif "lgbt" in user_input or "sexuality" in user_input:
        return "lgbt discrimination"
    else:
        return None

def get_option_response(crime_type, option):
    if option == "Understanding your rights":
        return responses["rights"].get(crime_type, "Rights information not available.")
    elif option == "How to report a crime":
        return responses["reporting_steps"].get("how_to_report", "Reporting steps not available.")
    elif option == "Local resources":
        return responses["resources"].get("mental_health", "No resources available.")
    elif option == "General information":
        return responses["definitions"].get(crime_type, "General information not available.")
    elif option == "Something else":
        return "Please specify your question further, and I'll try to help!"
    else:
        return "Invalid option."

# User input section
user_input = st.text_input("Describe the hate crime you experienced:")

if user_input:
    crime_type = get_crime_type(user_input)
    if crime_type:
        st.write(f"Detected hate crime type: {crime_type.capitalize()}")

        # Present options to the user
        st.write("Please choose one of the following options:")
        option = st.selectbox(
            "What would you like to know?",
            [
                "Understanding your rights",
                "How to report a crime",
                "Local resources",
                "General information",
                "Something else"
            ]
        )

        # Display response based on selected option
        if st.button("Get Information"):
            response = get_option_response(crime_type, option)
            st.write("Bot:", response)
    else:
        st.write("Sorry, I couldn't identify the type of hate crime. Please try describing it in more detail.")