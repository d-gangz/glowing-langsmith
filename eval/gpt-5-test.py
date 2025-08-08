"""
Demo script for using test GPT-5 model. Note that for best effect and for the chain of thought to be able to pass from one message to the next, you need to use the responses API.

check out this doc here: https://python.langchain.com/docs/integrations/chat/openai/#responses-api

LangChain collects all items in model_kwargs and merges them into the payload it sends to the OpenAI API. Provided the keys/structure match what the OpenAI API expects (see docs for OpenAI models), these fields will be available to the model.
"""

from langchain_openai import ChatOpenAI
from langsmith import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# llm = ChatOpenAI(model="gpt-5", use_responses_api=True)
# print(llm.invoke("Test message"))

# Initialize LangSmith client
client = Client()

# Pull the prompt with model settings included
prompt = client.pull_prompt("gpt5-test")

model = ChatOpenAI(
    model="gpt-5",
    # use_responses_api=True,
    output_version="responses/v1",
    reasoning={"effort": "minimal"},  # "minimal", "medium", "high"
    # text={"verbosity": "low"},  # "low", "medium", "high"
    model_kwargs={"text": {"verbosity": "high"}},  # "low", "medium", or "high"
)

print("model config:", model)

chain = prompt | model

# Invoke the prompt
result = chain.invoke(
    {
        "story": "A group of unlikely heroes must destroy a powerful ring by throwing it into a volcano while being pursued by evil forces"
    }
)

print("result:", result)
