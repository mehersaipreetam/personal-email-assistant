import ast
from typing import Annotated, Optional

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from langchain_core.messages import AIMessage
from mail import get_mails_content_tool
from prompts import SUMMARISE_EMAILS_PROMPT, GET_NEXT_NODE

llm_without_tools, llm_with_tools = None, None


class GraphState(TypedDict):
    all_responses: Annotated[list, add_messages]
    all_agents: Annotated[list, add_messages]
    user_query: Optional[str] = None
    mails: Optional[list] = None
    summary: Optional[str] = None


# Define the function that calls the model
def get_mails(state: GraphState):
    user_query = state["user_query"]
    mails_response = llm_with_tools.invoke(user_query)
    tool_calls = mails_response.additional_kwargs.get("tool_calls", False)
    mails = []
    if tool_calls:
        func = globals()[tool_calls[0]["function"]["name"]]
        args = ast.literal_eval(tool_calls[0]["function"]["arguments"])
        mails = func(**args)
    return {"mails": [str(mails)], "all_responses": [AIMessage(content=str(mails))], "all_agents": [AIMessage(content="get_mails")]}


def summarise(state: GraphState):
    static_prompt = SUMMARISE_EMAILS_PROMPT
    mails = state["mails"]
    summary = llm_without_tools.invoke(static_prompt + str(mails))
    return {"summary": summary, "all_responses": [AIMessage(content=str(summary))], "all_agents": [AIMessage(content="summarise")]}

def decide_next_node(state: GraphState):
    latest_response = state['all_responses'][-1].content
    all_agents = [s.content for s in state["all_agents"]]
    prompt = GET_NEXT_NODE.format(**{"user_query": state["user_query"][-1].content, "latest_response": latest_response, "all_agents": all_agents, "available_nodes": ["get_mails", "summarise"]})
    response = llm_without_tools.invoke(prompt)
    return response.content
    

def personal_email_assistant_graph(llm, user_query):
    # TODO: Add conditional edges, define next step function
    tools = [get_mails_content_tool]
    global llm_without_tools, llm_with_tools
    llm_without_tools = llm
    llm_with_tools = llm.bind_tools(tools)
    # Define a new graph
    workflow = StateGraph(GraphState)

    workflow.add_node("get_mails", get_mails)
    workflow.add_node("summarise", summarise) 

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point("get_mails")

    workflow.add_conditional_edges("get_mails", decide_next_node)

    workflow.add_edge("summarise", END)

    # Initialize memory to persist state between graph runs
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    final_state = app.invoke(
        {"user_query": [HumanMessage(content=user_query)]},
        config={"configurable": {"thread_id": 42}},
        debug=True,
    )
    response = final_state["summary"].content
    return response
