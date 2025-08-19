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
- [YT video on how command works](https://www.youtube.com/watch?v=6BJDKf90L9A)

---

**Bottom line:**

- Use a standard state schema with `todos` and `messages`.
- Messages should always go in the out-of-the-box `messages` array; LangGraph will handle agent output via those messages.
- Only the content of your ToolMessage (in `messages`) is rendered for the agent's/user's view, while `todos` are used internally for agent logic.

[1] https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/
[2] https://langchain-ai.github.io/langgraph/how-tos/graph-api/
[3] https://langchain-ai.github.io/langgraph/

# When to use `command` vs `conditional node`

Let’s go deeper into the **difference between Command and conditional nodes (conditional edges) in LangGraph**, and when to use each:

---

## What is a Conditional Node (Edge) in LangGraph?

- A **conditional node/edge** lets you route to the next node in your graph based on the _current state_.
- You set up logic that checks the state, and decides which node or nodes to go to next.
- It **does not modify the state itself**—routing is purely based on existing data.
- Examples: branching workflows, decision trees, simple if/else logic for next step.

**Syntax:**

```python
def conditional_routing(state: State) -> str:
    if state["foo"] == "bar":
        return "node_a"
    else:
        return "node_b"

graph.add_conditional_edges("current_node", conditional_routing)
```

- Here, the node itself doesn't change `foo`, it just picks what node to run next.

---

## What is a Command Node?

- A **Command** is special: it can **both update the graph state and decide what node to go to next – in the same node function**.
- This is great for more complex agent flows where you generate new data, update the state, and want the next step to depend on both things.
- Example: You process user input, generate a result, update the state with new information, and decide where to route next—all-in-one.

**Syntax:**

```python
def my_command_node(state: State) -> Command[Literal["node_a", "node_b"]]:
    if state["foo"] == "bar":
        return Command(update={"foo": "baz"}, goto="node_a")
    else:
        return Command(update={"foo": "qux"}, goto="node_b")
```

- This node both changes `foo` and picks the next route.

---

## Key Differences

| Aspect                    | Conditional Node/Edge          | Command Node                           |
| ------------------------- | ------------------------------ | -------------------------------------- |
| **Updates state?**        | ❌ No (read-only)              | ✅ Yes (can update state)              |
| **Control flow?**         | ✅ Yes (routes based on state) | ✅ Yes (routes based on state/results) |
| **Single step for both?** | ❌ No (only routing)           | ✅ Yes (combine update+routing)        |
| **Complex logic**         | ⚡ Ok for simple branching     | 🚀 Powerful for dynamic flows          |

---

## When to Use Which?

- Use **conditional node/edge** when:

  - You only need to decide the next node based on what’s already present in state—no update needed.
  - Example: Pure logic branching, e.g., “If user is authenticated, go to dashboard.”

- Use **Command** when:
  - You need to **both** update the state and choose where to route next, ideally in response to fresh data, output, or new side effects.
  - Example: After performing a calculation, update results and immediately route to a result display node.
  - Useful for scenarios like:
    - Multi-agent handoff (pass info + route)
    - Generating new data before branching
    - Compact dynamic agent workflows

---

## Practical Example

**Conditional edge:**

```python
# Separate logic for routing, no state update
def route_user(state: State) -> str:
    return "verify_account" if state["account_number"] else "ask_for_account"

graph.add_conditional_edges("start_node", route_user)
```

**Command node:**

```python
def process_ticket(state: State) -> Command[Literal["notify_user"]]:
    ticket_id = create_ticket(state["user_query"])
    return Command(
        update={"ticket_id": ticket_id},
        goto="notify_user"
    )
```

---

## References & Docs

- [LangGraph state graph node concepts (Command and conditional edges)](https://langchain-ai.github.io/langgraph/concepts/low_level/)[1]
- [LangGraph Glossary: difference and when to use Command vs conditional](https://langchain-ai.github.io/langgraphjs/concepts/low_level/)[2]
- [Control Flow tutorial including examples](https://www.linkedin.com/pulse/exploring-control-flow-langgraph-conditional-edges-vs-pranjal-dwivedi-emrjf)[3]

---

## TL;DR

- **Conditional node/edge = choose next step based only on current state.**
- **Command = update the state + choose next step (all in one).**

Use Command whenever you want to **do something and decide what happens next**, not just route.

[1] https://langchain-ai.github.io/langgraph/concepts/low_level/
[2] https://langchain-ai.github.io/langgraphjs/concepts/low_level/
[3] https://www.linkedin.com/pulse/exploring-control-flow-langgraph-conditional-edges-vs-pranjal-dwivedi-emrjf
[4] https://dev.to/jamesli/advanced-langgraph-implementing-conditional-edges-and-tool-calling-agents-3pdn
[5] https://towardsdatascience.com/from-basics-to-advanced-exploring-langgraph-e8c1cf4db787/
[6] https://www.reddit.com/r/LangChain/comments/1cn7cjy/changing_state_attributes_in_langgraph/
[7] https://langchain-ai.github.io/langgraph/how-tos/graph-api/
[8] https://github.com/langchain-ai/langgraph/discussions/5064
[9] https://github.com/langchain-ai/langgraph/discussions/2498
[10] https://www.youtube.com/watch?v=EKxoCVbXZwY
