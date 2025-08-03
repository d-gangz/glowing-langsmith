# LangSmith Dataset Creation Guide

This guide teaches you how to create and upload datasets to LangSmith for evaluation.

## What is a LangSmith Dataset?

A dataset in LangSmith is a collection of examples used to evaluate your LLM applications. Each example contains:
- **Inputs**: The data you pass to your prompt/chain
- **Outputs**: The expected results (optional for reference-free evaluation)
- **Metadata**: Additional info for filtering and analysis

## Dataset Format

Create a JSON file with a list of examples:

```json
[
  {
    "inputs": {
      "question": "What is 2+2?",
      "context": "Basic math"
    },
    "outputs": {
      "answer": "4"
    },
    "metadata": {
      "difficulty": "easy",
      "topic": "arithmetic"
    }
  }
]
```

## Creating a Dataset

### Step 1: Prepare Your Data

Create a JSON file with your examples. Each example should have:
- `inputs`: Dictionary with your input variables
- `outputs`: Dictionary with expected outputs (optional)
- `metadata`: Dictionary with any extra info (optional)

### Step 2: Upload to LangSmith

```python
import json
from langsmith import Client

# Load your data
with open("your_dataset.json", 'r') as f:
    examples = json.load(f)

# Create client
client = Client()

# Create dataset
dataset = client.create_dataset(
    dataset_name="Your Dataset Name",
    description="What this dataset tests"
)

# Upload examples
client.create_examples(dataset_id=dataset.id, examples=examples)
```

## Example: Movie Ratings Dataset

See `movie_ratings_dataset.json` for a complete example that:
- Takes movie descriptions and decades as inputs
- Expects movie ratings (G, PG, R) as outputs
- Includes metadata like title, genre, year

Run `python upload_dataset.py` to upload it.

## Tips

1. **Keep it simple**: Start with basic inputs/outputs, add metadata later
2. **Be consistent**: Use the same input/output keys across all examples
3. **Test small**: Start with 3-5 examples before creating large datasets
4. **Use metadata**: Add fields that help you filter and analyze results

## Common Use Cases

- **Classification**: Predict categories (like movie ratings)
- **Generation**: Generate text and compare to expected outputs
- **Extraction**: Extract information from text
- **Q&A**: Answer questions based on context

## Next Steps

After creating a dataset:
1. Use it in evaluations with `client.evaluate()`
2. View results in the LangSmith UI
3. Filter by metadata to analyze performance on subsets
4. Iterate and add more examples as needed