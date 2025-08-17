"""
Demo script for using test GPT-5 model with structured output using Pydantic. Note that for structured output, model_kwargs cannot be used.

Input data sources: LangSmith prompt "gpt5-test"
Output destinations: Console output with structured response
Dependencies: OpenAI API key, LangSmith API key
Key exports: MovieAnalysis (Pydantic model), structured analysis chain
Side effects: Makes API calls to OpenAI and LangSmith
"""

from langchain_openai import ChatOpenAI
from langsmith import Client
from dotenv import load_dotenv
from pydantic import BaseModel, Field


# Define Pydantic model for structured output
class MovieAnalysis(BaseModel):
    """Structured response for movie story analysis"""

    response: str = Field(description="The main response analyzing the movie story")
    genre: str = Field(
        description="The primary genre of the movie (e.g., Fantasy, Action, Drama)"
    )


# Load environment variables
load_dotenv()

# Initialize LangSmith client
client = Client()

# Pull the prompt with model settings included
prompt = client.pull_prompt("gpt5-test")

# Create model without model_kwargs for structured output compatibility
model = ChatOpenAI(
    model="gpt-5",
    output_version="responses/v1",
    reasoning={"effort": "minimal"},  # "minimal", "medium", "high"
    model_kwargs={"text": {"verbosity": "high"}},  # "low", "medium", or "high"
)

# Create structured output model
structured_model = model.with_structured_output(MovieAnalysis)

print("model config:", model)

# Create chain with structured output
chain = prompt | structured_model

# Invoke the prompt
result = chain.invoke(
    {
        "story": "A group of unlikely heroes must destroy a powerful ring by throwing it into a volcano while being pursued by evil forces"
    }
)

print("Structured result:")
print(f"Response: {result.response}")
print(f"Genre: {result.genre}")
print(f"Full result object: {result}")
