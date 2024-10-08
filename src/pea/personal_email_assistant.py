import ast
from typing import Annotated, Optional

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from langchain_core.messages import AIMessage
from mail import get_mails_content_tool
from prompts import SUMMARISE_EMAILS_PROMPT, GET_NEXT_NODE

llm_without_tools, llm_with_tools = None, None


class GraphState(TypedDict):
    """
    A TypedDict representing the state of a graph in the personal email assistant application.

    Attributes
    ----------
    all_responses : list
        A list that stores all the responses generated by the LLM or other agents.
    all_agents : list
        A list that contains all agents participating in the current graph's operations.
    user_query : str, optional
        The query entered by the user to search or filter emails.
    mails : list, optional
        A list containing the emails fetched or generated in response to the user query.
    summary : str, optional
        A summary of the emails or the result of the query, typically generated by the LLM.
    """
    all_responses: Annotated[list, add_messages]
    all_agents: Annotated[list, add_messages]
    user_query: Optional[str] = None
    mails: Optional[list] = None
    summary: Optional[str] = None


def get_mails(state: GraphState):
    """
    Retrieves emails based on the user's query and updates the graph state.

    Parameters
    ----------
    state : GraphState
        A dictionary-like object representing the current state of the graph, 
        including the user's query and other relevant information.

    Returns
    -------
    dict
        A dictionary containing the retrieved emails, responses, and agents, 
        structured as follows:
        
        - "mails": A list containing the retrieved emails as strings.
        - "all_responses": A list containing an AIMessage with the content of the emails.
        - "all_agents": A list containing an AIMessage indicating the function used.

    """
    user_query = state["user_query"]
    mails_response = llm_with_tools.invoke(user_query)
    tool_calls = mails_response.additional_kwargs.get("tool_calls", False)
    mails = []
    if tool_calls:
        func = globals()[tool_calls[0]["function"]["name"]]
        args = ast.literal_eval(tool_calls[0]["function"]["arguments"])
        mails = func(**args)
    return {
        "mails": [str(mails)],
        "all_responses": [AIMessage(content=str(mails))],
        "all_agents": [AIMessage(content="get_mails")],
    }


def summarise(state: GraphState):
    """
    Generates a summary of the emails stored in the graph state using a predefined prompt.

    Parameters
    ----------
    state : GraphState
        A dictionary-like object representing the current state of the graph, 
        including the emails that need to be summarized.

    Returns
    -------
    dict
        A dictionary containing the summary of the emails and updates to the graph state, 
        structured as follows:
        
        - "summary": The generated summary of the emails.
        - "all_responses": A list containing the summary.
        - "all_agents": A list containing an AIMessage indicating the function used.
    """
    static_prompt = SUMMARISE_EMAILS_PROMPT
    mails = state["mails"]
    summary = llm_without_tools.invoke(static_prompt + str(mails))
    return {
        "summary": summary,
        "all_responses": [summary],
        "all_agents": [AIMessage(content="summarise")],
    }


def decide_next_node(state: GraphState):
    """
    Generates a summary of the emails stored in the graph state using a predefined prompt.

    Parameters
    ----------
    state : GraphState
        A dictionary-like object representing the current state of the graph, 
        including the emails that need to be summarized.

    Returns
    -------
    dict
        A dictionary containing the summary of the emails and updates to the graph state, 
        structured as follows:
        
        - "summary": The generated summary of the emails.
        - "all_responses": A list containing the summary.
        - "all_agents": A list containing an AIMessage indicating the function used.
    """
    latest_response = state["all_responses"][-1].content
    all_agents = [s.content for s in state["all_agents"]]
    prompt = GET_NEXT_NODE.format(
        **{
            "user_query": state["user_query"][-1].content,
            "latest_response": latest_response,
            "all_agents": all_agents,
            "available_nodes": ["get_mails", "summarise"],
        }
    )
    response = llm_without_tools.invoke(prompt)
    if response.content == "END":
        return END
    return response.content


def personal_email_assistant_graph():
    """
    Constructs and compiles a state-based workflow for processing emails in a personal email assistant context.

    Returns
    -------
    object
        A compiled `StateGraph` application that represents the workflow, ready to be invoked with user queries.
    """
    workflow = StateGraph(GraphState)
    workflow.add_node("get_mails", get_mails)
    workflow.add_node("summarise", summarise)
    workflow.set_entry_point("get_mails")
    workflow.add_conditional_edges("get_mails", decide_next_node)

    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    return app

def personal_email_assistant(llm, user_query):
    """
    Processes a user query using a language model and a state-based workflow for a personal email assistant.

    Parameters
    ----------
    llm : object
        A language model object that will be used to process the user's query and interact with various tools.
    user_query : str
        The query provided by the user, intended to retrieve or process emails.

    Returns
    -------
    dict
        The final response generated by the workflow after processing the user's query, typically a summary or 
        a list of emails in a structured format.
    """
    tools = [get_mails_content_tool]
    
    global llm_without_tools, llm_with_tools
    llm_without_tools = llm
    llm_with_tools = llm.bind_tools(tools)

    app = personal_email_assistant_graph()

    final_state = app.invoke(
        {"user_query": [HumanMessage(content=user_query)]},
        config={"configurable": {"thread_id": 42}},
        debug=True,
    )

    response = final_state["all_responses"][-1].content
    if not isinstance(response, dict):
        response = ast.literal_eval(response)
    return response
