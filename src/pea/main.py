import argparse

from llm.llm_utils import get_llm
from pea.personal_email_assistant import personal_email_assistant_graph


def main():
    parser = argparse.ArgumentParser(description="Process the -url flag for an LLM.")
    parser.add_argument("-url", type=str, help="Specify the url")
    args = parser.parse_args()
    url = args.url

    user_query = input("Enter the query to your mailbox:\n")
    llm = get_llm(url=url, ollama_model="mistral")

    response = personal_email_assistant_graph(llm_model=llm, user_query=user_query)
    print("----------------------THIS IS THE RESPONSE----------------------")
    print(response)
    return


if __name__ == "__main__":
    main()
