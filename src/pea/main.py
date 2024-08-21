from langchain_ollama import ChatOllama

if __name__=="__main__":
    llm = ChatOllama(model="mistral", temperature=0)
    print(llm.invoke("Hi"))
