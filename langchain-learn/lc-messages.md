Absolutely! **LangGraph** provides pre-built patterns for message handling and conversation state ("messages plus" architecture). Here’s a fully up-to-date, beginner-friendly, yet production-realistic tutorial that shows **how to use messages and conversation state in LangGraph for multi-turn, multi-tool agentic systems**, following best practices.

---

# 🟦 LangGraph Agentic Workflow with Messages: Step-by-Step Guide

## 1. **What are Messages in LangGraph?**

LangGraph builds on LangChain’s message types:

- `HumanMessage`: user utterances
- `AIMessage`: assistant/LLM responses (including tool calls!)
- `ToolMessage`: output from a tool/function
- `SystemMessage`: system setup/behavior instructions

**All are subclasses of `BaseMessage`.** Messages are always stored in a list that represents the conversation state.

---

## 2. **State: The "Messages Plus" Pattern**

LangGraph recommends the “messages-plus” state:

- Your state dict always has a `messages` list (with type hints and auto-append behavior),
- Plus any extra keys you might need for your app.

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages  # auto-append utility

class State(TypedDict):
    # This ensures all messages (in/out, tool/AI/Human) are managed in order!
    messages: Annotated[list, add_messages]
    # Add any conversation-level fields you want, e.g.:
    name: str
    birthday: str
```

---

## 3. **Tool Definition (Tool Functions and Messages)**

LangGraph integrates with LangChain tools. Here’s a recommended tool definition style, including handling of tool call IDs automatically (best practice):

```python
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, InjectedToolCallId

@tool
def add(x: int, y: int, tool_call_id: InjectedToolCallId) -> str:
    """Add two numbers and explain the result."""
    total = x + y
    return ToolMessage(
        content=f"{x} + {y} = {total}",
        tool_call_id=tool_call_id  # critical for linking call/result!
    )
```

---

## 4. **Building the Graph (LLM Node, Tool Node) - Using LangGraph’s Primitives**

### (A) LLM Node: Handles user messages, emits AI messages & tool calls

```python
def llm_node(state: State):
    ai_message = llm_with_tools.invoke(state["messages"])  # Use LangChain LLMs/tools combo
    return {"messages": [ai_message]}
```

### (B) Tool Node: Executes pending tool calls (auto-handled by LangGraph)

```python
from langgraph.prebuilt import ToolNode, tools_condition

tool_node = ToolNode(tools=[add])  # tools auto-wired to their @tool function!
```

---

## 5. **Graph Wiring: Using "Conditional Edges" for Auto Tool Handling**

LangGraph recommends the following wiring for tool calling:

```python
from langgraph.graph import StateGraph, START

graph = StateGraph(State)
graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)

# Conditional edge: if tools are requested, route LLM output to tool node
graph.add_conditional_edges("llm", tools_condition)
# Otherwise, go back to llm after tool exec
graph.add_edge("tools", "llm")
# Kick off from START
graph.add_edge(START, "llm")

# Compile graph
compiled_graph = graph.compile()
```

---

## 6. **Running the Agent: See How Messages Evolve!**

```python
from langchain_core.messages import SystemMessage, HumanMessage

# Example: full context setup
state = {
    "messages": [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is 3 + 5?")
    ],
    "name": "",
    "birthday": ""
}
final_state = compiled_graph.invoke(state)

# Print all messages for the turn:
for msg in final_state["messages"]:
    print(f"{msg.type.upper()}: {msg.content}")
```

What happens under the hood:

- User sends message → stored as `HumanMessage`.
- LLM generates response; if a tool is needed, includes tool call in `AIMessage`.
- If tool call exists, tool is auto-invoked, result is wrapped as `ToolMessage` and appended to `messages`.
- LLM receives new state (with tool result in history) and produces a final user-facing `AIMessage`.
- The `messages` list in state reflects the _entire_ conversation history, including all tool reasoning!

---

## 7. **Extending with More Tools or Human-in-the-Loop**

Just add more `@tool`-decorated functions and include them in the `ToolNode`. Adapt your state dict to add fields as required for app context.

LangGraph's "messages-plus" approach means **your message history is always accurate and append-only**—important for production traceability or auditing.

---

# 🎯 **Summary Table: How LangGraph Handles Messages**

| Step                        | What’s Stored in `messages`?    | Message Types              |
| --------------------------- | ------------------------------- | -------------------------- |
| User Input                  | User’s utterance                | HumanMessage               |
| LLM Responds/Tool Call      | LLM reply (and any tool call)   | AIMessage                  |
| Tool Executes               | Tool’s output/result            | ToolMessage (linked by ID) |
| LLM Summarizes Final Output | LLM reply, now with all context | AIMessage                  |

---

# ✅ **Key Takeaways**

- **Always** use the pre-built messages plus pattern with `add_messages`.
- Let LangGraph route pending tool calls automatically—no glue code!
- The `messages` list is your ground truth for everything: user input, LLM reasoning, tools, system setup, and even human-in-the-loop corrections.
- This approach scales to _multi-agent_ and _multi-tool_ use cases seamlessly.

---

This design is not only idiomatic for LangGraph in 2025 but makes debugging, analytics, and observability via LangSmith super straightforward. The code above is both production-grade and easy to reason about—**use it as your go-to reference for stateful, agentic apps with real tool use in LangGraph**.

# Resources

1. Refer to the [Message Conceptual Guide](https://python.langchain.com/docs/concepts/messages/) to understand more
2. If you want to understand multi-modality, refer to this [Multimodality conceptual guide](https://python.langchain.com/docs/concepts/multimodality/).
3. Here's the [Tool calling conceptual guide](https://python.langchain.com/docs/concepts/tool_calling/)
