from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


@tool
def multiply(a: int, b: int):
    "Multiply two numbers."
    return a * b


llm = ChatOpenAI(model="gpt-4o-mini")
system_prompt = """You are a careful agent. Always explain your reasoning before making tool calls. If a tool fails, provide a helpful error message."""

agent = create_react_agent(
    model=llm,
    tools=[multiply],
    prompt=system_prompt,
)

# Run once (stateless)
result = agent.invoke({"messages": [HumanMessage(content="What is 8 * 7?")]})
print("Result:", result)

# To get the last element from the messages to pass back to the main agent:
messages = result["messages"]

final_answer = None
for message in reversed(messages):
    if isinstance(message, AIMessage):
        final_answer = message.content
        break

print("Final Answer:", final_answer)
