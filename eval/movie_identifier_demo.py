"""
Demo script for using the movie-identifier prompt from LangSmith
"""
import os
from langsmith import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LangSmith client
client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))

# Pull the prompt with model settings included
prompt = client.pull_prompt("movie-identifier", include_model=True)

# When include_model=True, the prompt already includes the model
# so we can use it directly as a chain
chain = prompt

# Two random movie examples
examples = [
    {
        "movie_description": "A group of unlikely heroes must destroy a powerful ring by throwing it into a volcano while being pursued by evil forces",
        "decade": "2000s"
    },
    {
        "movie_description": "An archaeologist with a whip searches for ancient biblical artifacts while fighting Nazis",
        "decade": "1980s"
    }
]

print("🎬 Movie Identifier Demo\n")
print("Using prompt:", "movie-identifier")
print("\n" + "="*50 + "\n")

# Process each example
for i, example in enumerate(examples, 1):
    print(f"Example {i}:")
    print(f"Description: {example['movie_description']}")
    print(f"Decade: {example['decade']}")
    
    # Invoke the prompt
    result = chain.invoke(example)
    
    print(f"Identified Movie: {result.content}")
    print("\n" + "-"*50 + "\n")

print("✅ Demo complete!")