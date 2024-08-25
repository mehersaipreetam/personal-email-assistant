from dotenv import load_dotenv

from llm import get_llm
from pea import personal_email_assistant_graph


def main():
    load_dotenv()
    user_query = input("Enter the query to your mailbox:\n")
    llm = get_llm()
    response = personal_email_assistant_graph(llm_model=llm, user_query=user_query)
    print("----------------------THIS IS THE RESPONSE----------------------")
    print(response)
    return response


if __name__ == "__main__":
    main()
