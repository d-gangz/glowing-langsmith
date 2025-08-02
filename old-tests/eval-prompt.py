from dotenv import load_dotenv
import os
from langsmith import Client

"""
This script evaluates a story outline generator using LangSmith.

Key purposes:
1. Load a stored prompt from LangSmith named "story-outline"
2. Create an evaluation function that invokes this prompt with inputs. Note that invoke has no streaming hence there is no time to first token.
3. Run an evaluation using a pre-existing dataset
4. Log all interactions to LangSmith for analysis

Requires:
- A LangSmith account with API key
- A stored prompt named "story-outline" in your LangSmith account
- A dataset named "story input" in your LangSmith account
"""

# Load environment variables including LANGSMITH_API_KEY
load_dotenv()

# Initialize LangSmith client with API key from environment
client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
    
# Pull the story-outline prompt from LangSmith
# include_model=True means it will include the model configuration
# This returns a RunnableSequence that can be executed
prompt = client.pull_prompt("story-outline", include_model=True)
# Alternative prompt that can be uncommented if needed
# prompt = client.pull_prompt("story-outline-4omini", include_model=True)

# Define the target function that will be evaluated by LangSmith
def story_outline_generator(inputs):
    """
    Process inputs through the prompt and return the result.
    
    Args:
        inputs: Dictionary containing input values from the dataset
                (likely including 'genre' and 'context' keys)
    
    Returns:
        The generated story outline
    """
    # The inputs will be provided by LangSmith from the dataset
    return prompt.invoke(inputs)

# Run the evaluation using LangSmith's evaluate method
evaluation_results = client.evaluate(
    story_outline_generator,           # The function to evaluate
    data="story input",                # The dataset name in LangSmith
    experiment_prefix="story-outline-evaluation"  # Prefix for the experiment name
)