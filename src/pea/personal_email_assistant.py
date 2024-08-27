from typing import Annotated

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from mail import get_mails_content_tool
from prompts import SUMMARISE_EMAILS_PROMPT

llm_without_tools, llm_with_tools = None, None


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Define the function that calls the model
def get_mails(state: MessagesState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def summarise(state: MessagesState):
    static_prompt = SUMMARISE_EMAILS_PROMPT
    messages = state["messages"][-1].content
    response = llm_without_tools.invoke(static_prompt + str(messages))
    return {"messages": [response]}


def personal_email_assistant_graph(llm, user_query):
    tools = [get_mails_content_tool]
    tool_node = ToolNode(tools)
    global llm_without_tools, llm_with_tools
    llm_without_tools = llm
    llm_with_tools = llm.bind_tools(tools)
    # Define a new graph
    workflow = StateGraph(MessagesState)

    workflow.add_node("get_mails", get_mails)
    workflow.add_node("summarise", summarise)
    workflow.add_node("tools", tool_node)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point("get_mails")

    workflow.add_edge("get_mails", "tools")

    workflow.add_edge("tools", "summarise")

    workflow.add_edge("summarise", END)

    # Initialize memory to persist state between graph runs
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    final_state = app.invoke(
        {"messages": [HumanMessage(content=user_query)]},
        config={"configurable": {"thread_id": 42}},
        debug=True,
    )
    response = final_state["messages"][-1].content
    return response
