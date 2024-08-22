from typing import Annotated

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from mail.mail_util import get_mails_content_tool


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Define the function that calls the model
def get_mails(state: MessagesState):
    messages = state["messages"]
    response = llm.invoke(messages)
    print("Got the mails")
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


def summarise(state: MessagesState):
    static_prompt = "You are a personalised mail assistant. Given the below mails, your job is to summarise them each in not more than 2 sentences and output them in order. Make sure for each summary, you provide from, date, subject and the final summary of that mail. The output must be in the format {'from': <from>, 'subject': <subj>, 'datetime': <datetime>, 'summary': <summary>}"
    messages = state["messages"]
    print(messages)
    response = llm.invoke(static_prompt + str(messages))
    print("Summarisation done")
    return {"messages": [response]}


def personal_email_assistant_graph(llm_model, user_query):
    tools = [get_mails_content_tool]
    tool_node = ToolNode(tools)
    global llm
    llm = llm_model.bind_tools(tools)
    # Define a new graph
    workflow = StateGraph(MessagesState)

    workflow.add_node("get_mails", get_mails)
    workflow.add_node("summarise", summarise)
    workflow.add_node("tools", tool_node)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point("get_mails")
    workflow.add_conditional_edges(
        "get_mails",
        tools_condition,
    )
    workflow.add_edge("tools", "get_mails")

    workflow.add_edge("get_mails", "summarise")

    workflow.add_edge("summarise", END)

    # Initialize memory to persist state between graph runs
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    final_state = app.invoke(
        {"messages": [HumanMessage(content=user_query)]},
        config={"configurable": {"thread_id": 42}},
    )
    response = final_state["messages"][-1].content
    return response
