from langchain_groq import ChatGroq


def get_llm(model="llama-3.1-70b-versatile"):
    llm = ChatGroq(
        model=model,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return llm
