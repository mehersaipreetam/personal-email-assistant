import streamlit as st
from dotenv import load_dotenv

from llm import get_llm
from pea import personal_email_assistant_graph


def main():
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

            # Display the response
            st.write("**Response:**")
            st.text(response)
        else:
            st.warning("Please enter a query.")


if __name__ == "__main__":
    main()
