import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from llm import get_llm
from pea import personal_email_assistant_graph

# Set the page layout to wide
st.set_page_config(layout="wide")


def format_email_data(email_data):
    """
    Pretty print the email dictionary content.
    """
    formatted_string = ""
    for i, email in enumerate(email_data, 1):
        formatted_string += f"### Email {i}\n\n"
        for key, value in email.items():
            formatted_string += f"**{key.capitalize()}:** {value}\n\n"
        formatted_string += "---\n\n"
    return formatted_string


def main():
    """
    Main streamlit app function for the project
    """
    # Load environment variables
    load_dotenv()

    # Create a Streamlit text input for the user query
    user_query = st.text_input("Enter the query to your mailbox:")

    # Create a button to submit the query
    if st.button("Submit"):
        if user_query:
            # Get the LLM model
            llm = get_llm()

            # Get the response from the personal email assistant graph
            response = personal_email_assistant_graph(llm=llm, user_query=user_query)

            # Display the email data from the response dynamically
            if response:
                st.write("### Emails Overview")

                # Format and pretty print the email data
                formatted_response = format_email_data(response)
                st.markdown(formatted_response)
            else:
                st.warning("No emails found for the given query.")
        else:
            st.warning("Please enter a query.")


if __name__ == "__main__":
    main()
