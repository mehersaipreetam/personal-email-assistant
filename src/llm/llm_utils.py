from langchain_ollama import ChatOllama


def get_llm(url, ollama_model="mistral"):
    llm = ChatOllama(model=ollama_model, temperature=0, base_url=url)
    return llm
