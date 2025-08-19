"""
Demo script for using test GPT-5 model with structured output using Pydantic. Note that for structured output, model_kwargs cannot be used.

Input data sources: LangSmith prompt "gpt5-test"
Output destinations: Console output with structured response
Dependencies: OpenAI API key, LangSmith API key
Key exports: MovieAnalysis (Pydantic model), structured analysis chain
Side effects: Makes API calls to OpenAI and LangSmith
"""

from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
from langsmith import Client
from dotenv import load_dotenv
from pydantic import BaseModel, Field


# Load environment variables
load_dotenv()

# Initialize LangSmith client
client = Client()

# Pull the prompt with model settings included
prompt = client.pull_prompt("util__user-intent-handler", include_model=True)

# Create chain with structured output
# chain = prompt.with_config({"run_name": "user-intent-handler"})

chain = prompt

# Invoke the prompt
result = chain.invoke(
    {
        "final_message": "I want some scones next",
        "previous_messages": "thanks for delivering the ice crea,",
    }
)

print("Structured result:")
print(f"Response: {result}")
