#!/usr/bin/env python3
"""
Upload movie ratings dataset to LangSmith
"""

import json
from langsmith import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load JSON data
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "movie_ratings_dataset.json")
with open(json_path, 'r') as f:
    examples = json.load(f)

# Initialize LangSmith client
client = Client()

# Create dataset
dataset = client.create_dataset(
    dataset_name="Movie Ratings Dataset",
    description="Movie rating predictions based on descriptions and decades"
)

# Upload examples
client.create_examples(dataset_id=dataset.id, examples=examples)

print(f"✅ Created dataset '{dataset.name}' with {len(examples)} examples")
print(f"Dataset ID: {dataset.id}")