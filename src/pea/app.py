import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from llm import get_llm
from pea import personal_email_assistant_graph, personal_email_assistant

# Set the page layout to wide
st.set_page_config(layout="wide")


def format_email_data(email_data):
    """
    Formats and pretty prints the content of a list of email dictionaries.

    Parameters
    ----------
    email_data : list of dict
        A list of dictionaries where each dictionary contains key-value pairs
        representing the details of an email (e.g., subject, sender, date, etc.).

    Returns
    -------
    str
        A formatted string where each email is presented with its details
        in a human-readable format, with each email separated by a line.
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

    This function serves as the entry point for the Streamlit app, allowing users to query their mailbox
    and view formatted email data based on their input.
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
            response = personal_email_assistant(llm=llm, user_query=user_query)

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
