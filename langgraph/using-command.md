# How `Command` works

Here’s a **comprehensive explanation** of how `Command` works in LangGraph, especially in the _Create React agent + tool message output_ use case we’ve discussed.

---

## What is `Command` in LangGraph?

- **`Command`** is a special return type for nodes (like your tool functions), giving you **explicit control** over:
  1. **State updates** (update values, arrays, messages, etc.)
  2. **Control flow/routing** (optionally specify which node comes next)
  3. **Structured agent response** (especially for defining what message/result the agent should return)

This is different from the standard automatic wrapping where LangGraph/React agent would simply return the raw result as a `ToolMessage`.

---

## How Does `Command` Work in Tool Nodes?

- Your tool function (e.g., `write_todos`) is called by LangGraph when an agent needs to perform some action.
- If your tool returns a `Command(update={...})`, **LangGraph updates the graph/state** with whatever keys you specify (e.g., `"todos"`, `"messages"`).
- When used in combination with a Create React agent, the **agent will look for any `ToolMessage` objects in your `messages` state**—those become the agent’s output.

### Example Flow

1. **User makes a request.**
2. React agent determines a `write_todos` tool call is needed.
3. `write_todos` is called, returning:
   ```python
   return Command(
      update={
         "todos": todos,
         "messages": [
            ToolMessage(f"Updated todo list to {todos}", tool_call_id=tool_call_id)
         ]
      }
   )
   ```
4. The agent:
   - **Updates internal state** (`todos` and `messages`).
   - **Returns only `ToolMessage`(s) in `messages` state as its output**, not the raw state.

---

## Why use `Command` for this?

- **Gives you control**: You decide what the user or downstream agent sees, writes, or acts on.
- **Avoids double output/nested messages**: Only your chosen message(s) are returned, not automatic wrappers or full state payload.
- **Keeps state clean for workflow**: You can hold/record data for future agent steps, but only output what you want immediately visible.

---

## Key Behavior for Create React Agent

- **Agent output ≈ `messages` you define in the command's update**
- `Command` allows tool nodes to update the state _and_ specify an illustrative message (summary, structured result, markdown, raw array—your choice).
- No nested/double wrapping: if you want the updated array returned to the user, include its representation in the message content.

---

## Official Documentation & Further Reading

- [LangGraph Command API Documentation (TypeScript/Javascript)](https://langchain-ai.github.io/langgraphjs/reference/classes/langgraph.Command.html)[1]
- [How to Update Graph State from Tools (includes createReactAgent examples)](https://langchain-ai.github.io/langgraphjs/how-tos/update-state-from-tools/)[2]
- [LangChain Blog: Command for Multi-Agent Architectures](https://blog.langchain.dev/command-a-new-tool-for-multi-agent-architectures-in-langgraph/)[3]

**These guides will show you design patterns—both in Python and JS/TS—that demonstrate updating state and returning messages in LangGraph agents.**

---

## Best Practice Recap

- **Use `Command`** for tool nodes when you want custom state updates and controlled output.
- **Create React agent reads messages in state, not entire state for output.**
- **Message content = user-facing result.**
- State keys (e.g., `todos`) stay _internal_ unless explicitly represented in a message.

Let me know if you want a more advanced example or tips on how to structure your message content for certain UI or downstream processing!

[1] https://langchain-ai.github.io/langgraphjs/reference/classes/langgraph.Command.html
[2] https://langchain-ai.github.io/langgraphjs/how-tos/update-state-from-tools/
[3] https://blog.langchain.dev/command-a-new-tool-for-multi-agent-architectures-in-langgraph/
[4] https://docs.langchain.com/langgraph-platform/cli
[5] https://www.langchain.com/langgraph
[6] https://docs.langchain.com/langgraph-platform/langgraph-cli
[7] https://www.getzep.com/ai-agents/langgraph-tutorial/
[8] https://langchain-ai.github.io/langgraph/
[9] https://www.reddit.com/r/LangChain/comments/1f8ui4a/tool_calling_in_langgraph_and_how_to_update_the/
[10] https://www.agentuity.com/blog/langgraph-structured-output

# How LangGraph’s Command Updates State and Messages for a To-Do Agent

Absolutely—let’s make this more realistic for your to-do manager agent in LangGraph, given that:

- Your state will definitely include a `todos` list.
- For messages, you’d use LangGraph’s standard, out-of-the-box `messages` state (which handles workflow and tool messages for you).

---

## Realistic State Schema Example

Here’s how you’d typically define the state:

```python
from typing import TypedDict, List
from langgraph.schema import Message  # Standard LangGraph message class

class State(TypedDict):
    todos: List[str]
    messages: List[Message]  # Use the built-in Message type
```

- `todos`: Your array of todo items.
- `messages`: The standard field LangGraph uses to record agent/LLM/tool/toolcall messages.

---

## Realistic Tool Function Example

When your tool (node) wants to update todos and communicate its result, you’d do:

```python
from langgraph.graph import Command
from langgraph.schema import ToolMessage

def write_todos(todos: list[str], tool_call_id: str) -> Command:
    return Command(
        update={
            "todos": todos,  # Update the todo list in state.
            "messages": [
                ToolMessage(
                    content=f"Updated todo list to {todos}",
                    tool_call_id=tool_call_id
                )
            ]
        }
    )
```

### Why this works

- `"todos"`: Directly updates the todo list (for agent reasoning, future workflow steps, API, etc.).
- `"messages"`: Uses the standardized LangGraph message queue so your tool’s output appears for both the agent and the user interface.

---

## Agent Output Behavior

- **Agent output**: What the user/conversation sees is determined by what’s inside `messages` (managed by LangGraph).
- The result is **not** the raw `todos` list, but the ToolMessage you put into `messages`.
- If you want to display the to-do list, format it in the message content, e.g., `"Your updated todo list: ..."`.
- The underlying state (the `todos` array) is there for any future agent step or external inspection.

---

## The Flow: Step-by-Step

1. **Initial State:**
   ```python
   {
       "todos": ["buy milk"],
       "messages": []
   }
   ```
2. **After agent executes `write_todos`:**
   ```python
   {
       "todos": ["buy milk", "walk dog"],
       "messages": [
           ToolMessage(
               content="Updated todo list to ['buy milk', 'walk dog']",
               tool_call_id="abc123"
            )
       ]
   }
   ```
3. **Agent output:** Only returns what’s in `messages`.

---

## Relevant Docs

- [Message state and workflow management in LangGraph](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/)[1]
- [How message management works in LangGraph](https://langchain-ai.github.io/langgraph/how-tos/graph-api/)[2]
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)[3]

---

**Bottom line:**

- Use a standard state schema with `todos` and `messages`.
- Messages should always go in the out-of-the-box `messages` array; LangGraph will handle agent output via those messages.
- Only the content of your ToolMessage (in `messages`) is rendered for the agent's/user's view, while `todos` are used internally for agent logic.

[1] https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/
[2] https://langchain-ai.github.io/langgraph/how-tos/graph-api/
[3] https://langchain-ai.github.io/langgraph/
