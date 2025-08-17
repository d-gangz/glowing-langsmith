Here is an updated, accurate, and practical tutorial for using LangGraph’s `create_react_agent`, reflecting the **actual output structure** you are seeing—where the result is a dictionary with a `"messages"` key containing a list of message objects (such as `HumanMessage`, `AIMessage`, and `ToolMessage`).

---

# 👩💻 Comprehensive Tutorial: LangGraph `create_react_agent` (Python, 2025 Edition)

---

## 1. **What is `create_react_agent`?**

- **Purpose:** Creates a "ReAct" agent that reasons step-by-step and can call tools/functions. Internally, it builds a trace of all thoughts, tool calls, and tool results.
- **Typical usage:** Standalone agent, or as a sub-agent (that you can plug into larger graphs or other agents).

---

## 2. **How to Install & Import**

```python
# Install latest (if needed)
# pip install langgraph langchain-openai

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
```

---

## 3. **Defining Tools**

Each tool should be a function with type hints and a docstring:

```python
@tool
def multiply(a: int, b: int):
    "Multiply two numbers."
    return a * b
```

---

## 4. **Creating the Agent (with System Prompt)**

Use the `prompt` parameter to set the agent’s system prompt at creation:

```python
llm = ChatOpenAI(model="gpt-4o-mini")
system_prompt = """You are a careful agent. Always explain your reasoning before making tool calls. If a tool fails, provide a helpful error message."""

agent = create_react_agent(
    model=llm,
    tools=[multiply],
    prompt=system_prompt  # Set your prompt here
)
```

---

## 5. **How to Call the Agent**

**ALWAYS pass input as a `messages` list**. The most reliable and compatible format is:

```python
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is 8 * 7?"}
    ]
})
```

---

## 6. **Understanding the Output**

- The returned object is a dictionary with a single `"messages"` key.
- `"messages"` is a list of message objects (not plain dicts), typically:
  - `HumanMessage` for input,
  - `AIMessage` for model "thoughts" and answers,
  - `ToolMessage` for each tool's output/observation.

---

## 7. **Getting the Final Answer**

- **The final agent response is the last `AIMessage` in `result["messages"]`.**
- Here’s how you extract it:

```python
from langchain_core.messages import AIMessage

messages = result["messages"]
final_answer = None
for msg in reversed(messages):
    if isinstance(msg, AIMessage):
        final_answer = msg.content
        break

print("Final Answer:", final_answer)
```

If you can’t import `AIMessage`, a generic filter also works:

```python
final_answer = None
for msg in reversed(result["messages"]):
    # Make sure it's a model message, not a tool/human
    # ToolMessage usually has a .name or .tool_call_id
    if hasattr(msg, "content") and not hasattr(msg, "name"):
        final_answer = msg.content
        break

print("Final Answer:", final_answer)
```

---

## 8. **How to Understand Each Message**

Each message in `result["messages"]` describes a step:

- **HumanMessage**: user input,
- **AIMessage**: Thoughts, decisions, or final answer,
- **ToolMessage**: Results from tools.

You can inspect the entire reasoning chain if you want to debug or visualize the agent's process.

---

## 9. **Reusable Utility Function**

Here’s a function you can use in your projects:

```python
def extract_final_answer(agent_result):
    for msg in reversed(agent_result["messages"]):
        if hasattr(msg, "content") and not hasattr(msg, "name"):
            return msg.content
    return None
```

---

## 10. **Sample Full Usage**

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def multiply(a: int, b: int):
    "Multiply two numbers."
    return a * b

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_react_agent(
    model=llm,
    tools=[multiply],
    prompt="Always explain your thought process and show intermediate steps."
)

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is 8 * 7?"}
    ]
})

# Print full trace
for m in result["messages"]:
    print(f"[{type(m).__name__}]: {getattr(m, 'content', '')}")

# Extract just the final output
print("Final Answer:", extract_final_answer(result))
```

---

## 11. **FAQ & Troubleshooting**

- **Q:** What if there is no `"output"` key?  
  **A:** Use the method above to extract the answer from `messages` (the final `AIMessage.content`).
- **Q:** How do I pass a system prompt?  
  **A:** Always use the `prompt=` parameter at agent creation.
- **Q:** What if I want the full agent reasoning chain?  
  **A:** Use the list in `result["messages"]`.

---

## 12. **Summary Table**

| What you want     | What you do                                                   |
| ----------------- | ------------------------------------------------------------- |
| Create agent      | Use `create_react_agent(model, tools, prompt)`                |
| Set system prompt | Pass your text as `prompt`                                    |
| Call agent        | `.invoke({"messages": [{"role": "user", "content": "..."}]})` |
| Final answer only | Last `AIMessage` in `result["messages"]` (`.content` field)   |
| Full trace        | Iterate over `result["messages"]`                             |

---

**Now this tutorial accurately matches the actual output you see in practice with modern LangGraph!**  
Let me know if you want example code for visualizing the whole agent trace or plugging this into a larger graph/multi-agent system.
