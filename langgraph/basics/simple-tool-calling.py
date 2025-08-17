from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# system_message = SystemMessage(content="You are a helpful assistant.")
# human_message = HumanMessage(content="What is the capital of France?")
# tool_message = ToolMessage(content="The capital of France is Paris.", tool_call_id="0")

# messages = [system_message, human_message, tool_message]

# print(messages)


# Define tools*
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# LLM with both tools bound*
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools([add, multiply])


# Agent Node: calls LLM and adds the assistant's message to state*
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Build Graph*
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)

# Register both tools with ToolNode*
builder.add_node("tools", ToolNode([add, multiply]))

# Workflow edges: Start → LLM → (tools OR END based on tools_condition)*
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,  # checks if assistant's latest message is a tool call. If it is, it will go directly to the tools node, else it will go to the END node. This is a prebuild thing.
)
builder.add_edge("tools", END)

# Compile*
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

messages = [HumanMessage(content="Hello, what is 2 multiplied by 2?")]
messages = graph.invoke({"messages": messages})

messages = [HumanMessage(content="Hello, what is 10 plus 2?")]
messages = graph.invoke({"messages": messages})

for m in messages["messages"]:
    m.pretty_print()
