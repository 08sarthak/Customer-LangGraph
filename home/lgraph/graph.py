from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from home.lgraph.AgentState import final_tools
from home.utilities import create_tool_node_with_fallback
from home.lgraph.AgentState import Assistant,assistant_set,State
from home.lgraph.AgentState import tool_set


def tool_set2():
    '''
    if not final_tools:
        print("Final tool  NOT SET:", final_tools)
        tool_set()
        print("Final tool  NOT SET 2:", final_tools)
    '''
    builder = StateGraph(State)

    # Define nodes: these do the work
    print("Final tool set:", final_tools)
    part_1_assistant_runnable=assistant_set()
    builder.add_node("assistant", Assistant(part_1_assistant_runnable))
    print("1.1")
    builder.add_node("tools", create_tool_node_with_fallback(final_tools))
    # Define edges: these determine how the control flow moves
    print("1.2")
    builder.add_edge(START, "assistant")
    print("1.3")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    print("1.4")
    builder.add_edge("tools", "assistant")
    # The checkpointer lets the graph persist its state
    # this is a complete memory for the entire graph.
    memory = SqliteSaver.from_conn_string(":memory:")
    part_1_graph = builder.compile(checkpointer=memory)

    return part_1_graph