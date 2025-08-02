from dotenv import load_dotenv
import os
from langsmith import Client

"""
This script is used to generate a story outline based on the given genre and context.
It uses the LangSmith API to pull the story-outline prompt and prompt.invoke it with the provided genre and context.

So note that you need to input your own GOOGLE_API_KEY and also install the landchain-google-gen-ai dependency. Probably the model=true only gives you the parameter for the model. The AI API is managed by yourself.
"""

def generate_story_outline(genre, context):
    """
    Generate a story outline based on the given genre and context.
    
    Args:
        genre (str): The genre of the story (e.g., "horror", "fantasy")
        context (str): The context or setting for the story
        
    Returns:
        The generated story outline
    """
    load_dotenv()
    client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
    
    # Pull the story-outline prompt from LangSmith
    # prompt = client.pull_prompt("story-outline", include_model=True)
    prompt = client.pull_prompt("story-outline-4omini", include_model=True)
    
    # Invoke the prompt with the provided genre and context
    return prompt.invoke({"genre": genre, "context": context})


def run():
    """Run the story outline generator with sample inputs."""
    genre = "horror"
    context = "A group of friends go on a camping trip to a remote forested area."
    
    story_outline = generate_story_outline(genre, context)
    
    # Format the output for better readability in terminal
    print("\n=== STORY OUTLINE ===\n")
    print(f"Content:\n{story_outline.content}")
    print("\n=== METADATA ===")
    
    # Display all available metadata attributes
    for key, value in story_outline.__dict__.items():
        if key != "content" and not key.startswith("_"):
            print(f"{key}: {value}")
    
    print("\n====================\n")
    
    
if __name__ == "__main__":
    run()