from langchain_groq import ChatGroq


def get_llm(model="llama3-70b-8192"):
    llm = ChatGroq(
        model=model,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return llm
