import os
import asyncio
from dotenv import load_dotenv
from langsmith import Client
from typing import Dict, Any

"""
This script demonstrates how to use LangSmith to evaluate a streaming LLM prompt execution.

Key purposes:
1. Show how to properly handle streaming outputs in LangSmith evaluations
2. Measure time to first token and other streaming performance metrics
3. Compare with non-streaming prompt.invoke() method which doesn't show streaming metrics
4. Log all streaming interactions to LangSmith for analysis

Requires:
- A LangSmith account with API key
- A stored prompt named "story-outline" in your LangSmith account
- A dataset named "story input" in your LangSmith account
"""

# Load environment variables including LANGSMITH_API_KEY
load_dotenv()

# Initialize LangSmith client
client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))

# Pull the stored prompt from LangSmith
# include_model=True means it will include the model configuration
# This returns a RunnableSequence that can be executed
prompt = client.pull_prompt("story-outline", include_model=True)

# Define the async function that will be evaluated by LangSmith
async def story_outline_generator(inputs: Dict[str, Any]) -> str:
    """
    Process inputs through the prompt with streaming and return the complete result.
    
    Args:
        inputs: Dictionary containing input values from the dataset
                (likely including 'genre' and 'context' keys)
    
    Returns:
        The complete generated text as a single string
    """
    # Initialize empty result string to collect all chunks
    result = ""
    
    # Stream the response asynchronously
    # prompt.astream() returns chunks one by one as they're generated
    async for chunk in prompt.astream(inputs):
        # Each chunk is an AIMessageChunk object, not a raw string
        # We need to extract the text content before concatenating
        if hasattr(chunk, "content"):
            # For chat models, chunks have a content attribute
            result += chunk.content
        else:
            # Fallback for other chunk types
            result += str(chunk)
            
        # Note: In a real application, you might want to yield each chunk to the user
        # immediately, rather than waiting for the complete response
    
    # Return the complete assembled response
    return result

# Define the async function to run the evaluation
async def run_evaluation():
    """
    Run the async evaluation process using LangSmith's aevaluate.
    
    Returns:
        The evaluation results object
    """
    # client.aevaluate is the async version of evaluate
    # It allows us to properly evaluate async functions
    evaluation_results = await client.aevaluate(
        story_outline_generator,       # The async function to evaluate
        data="story input",            # The dataset name in LangSmith
        experiment_prefix="story-outline-stream",  # Prefix for the experiment name
        max_concurrency=2              # Run up to 2 evaluations concurrently
    )
    return evaluation_results

# Execute the evaluation when run directly
if __name__ == "__main__":
    # asyncio.run is required to run async functions from synchronous code
    evaluation_results = asyncio.run(run_evaluation())
    
    # Output could be added here to display results
    # print(f"Evaluation complete. View results at: {evaluation_results.url}")
