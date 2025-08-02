import os
import asyncio
import json
from dotenv import load_dotenv
from langsmith import Client, traceable
from typing import Dict, Any

"""
This script demonstrates how to use LangSmith to evaluate a streaming LLM prompt execution.

Key purposes:
1. Show how to properly handle streaming outputs in LangSmith evaluations
2. Measure time to first token and other streaming performance metrics
3. Compare with non-streaming prompt.invoke() method which doesn't show streaming metrics
4. Log all streaming interactions to LangSmith for analysis
5. Demonstrate proper input structure for LangSmith UI visualization
6. Show how to pass direct parameters to a traced function instead of nested inputs

Requires:
- A LangSmith account with API key
- A stored prompt named "fullstory" in your LangSmith account

Notes:
- The prompts returns a streaming JSON object.
- Using direct parameters (context, outline) creates a cleaner UI experience in LangSmith.
- Parameters are mapped to a dictionary internally for compatibility with prompt expectations.
"""

# Load environment variables including LANGSMITH_API_KEY
load_dotenv()

# Initialize LangSmith client
client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))

# Pull the stored prompt from LangSmith
# include_model=True means it will include the model configuration
# This returns a RunnableSequence that can be executed
full_story_prompt = client.pull_prompt("fullstory", include_model=True)

@traceable(run_type="llm", name="full_story_generator")
async def full_story_generator(context: str, outline: str) -> Dict[str, str]:
    """
    Process inputs to generate a complete story with reasoning.
    
    Args:
        context: The context or setting for the story
        outline: The outline of the story
    
    Returns:
        A dictionary with 'reason' and 'output' keys
    """
    # Collect the final chunk which will contain the complete response
    final_chunk = None
    
    # Create inputs dictionary for the prompt
    inputs = {
        "context": context,
        "outline": outline
    }
    
    # Stream the response asynchronously
    async for chunk in full_story_prompt.astream(inputs):
        # print(chunk)
        # Simply save the most recent chunk - the last one will have the complete response
        final_chunk = chunk
    
    # Return the final chunk which has the complete response in the exact format
    return final_chunk

# Sample inputs for testing
SAMPLE_CONTEXT = "Set in near-future San Francisco where AI technology has become advanced but still not fully trusted by society."
SAMPLE_OUTLINE = "A young programmer discovers an AI that can predict the future but struggles with the moral implications of using this knowledge."

# Execute the story generation when run directly
async def main():
    print("Generating full story from context and genre...")
    print(f"\nCONTEXT: {SAMPLE_CONTEXT}")
    print(f"\nOUTLINE: {SAMPLE_OUTLINE}")
    
    print("\nGenerating story...")
    result = await full_story_generator(SAMPLE_CONTEXT, SAMPLE_OUTLINE)
    
    print("\nFinal result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    # asyncio.run is required to run async functions from synchronous code
    asyncio.run(main())
