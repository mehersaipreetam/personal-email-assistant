from langchain_groq import ChatGroq


def get_llm(model="llama3-70b-8192"):
    """
    Initializes and returns an instance of the ChatGroq LLM with specified configurations. Support for other LLMs can be added as well

    Parameters
    ----------
    model : str, optional
        The name of the language model to be used (default is "llama3-70b-8192").

    Returns
    -------
    ChatGroq
        An instance of the ChatGroq LLM configured with the specified parameters.
    """
    llm = ChatGroq(
        model=model,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return llm
