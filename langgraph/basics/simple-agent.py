"""
This is a simple example of a Langgraph agent that uses tools to perform arithmetic operations.

Utilize the ` @tool` decorator to define the tool with the tools description.

Note that currently within the Langsmith Traces, you are not able to see the tool descriptions. It is a choice by the Langsmith team, I think.
"""

from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


print(multiply.name)
print(
    multiply.description
)  # The function docstring is being taken in as the tool description.


# @tool("add_numbers", description="Adds a and b.")
@tool("add_numbers")
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


print(add.name)
print(add.description)


@tool
def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b


tools = [add, multiply, divide]
llm = ChatOpenAI(model="gpt-4o")

# For this ipynb we set parallel tool calling to false as math generally is done sequentially, and this time we have 3 tools that can do math
# the OpenAI model specifically defaults to parallel tool calling for efficiency, see https://python.langchain.com/docs/how_to/tool_calling_parallel/
# play around with it and see how the model behaves with math equations!
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

# System message
sys_msg = SystemMessage(
    content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
)


# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


# Build graph and add nodes
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Workflow edges: Start → Assistant → (tools OR END based on tools_condition)*
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# This is a sample of a custom condition
# def custom_tools_condition(state):
#     """Route based on whether the LLM issued a tool call in the last message."""
#     # Check the last message from LLM
#     last_message = state["messages"][-1]

#     # For OpenAI-style tools, a tool call is signaled via `tool_calls` or similar
#     if hasattr(last_message, "tool_calls") and last_message.tool_calls:
#         return "tools"    # Go to tools node
#     else:
#         return "other_node"  # Your custom node (or whatever you name it)


# Compile*
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

# Invoke messages to show
messages = [
    HumanMessage(
        content="Add 3 and 4. Multiply the output by 2. Divide the output by 5"
    )
]
messages = graph.invoke({"messages": messages})

for m in messages["messages"]:
    m.pretty_print()
