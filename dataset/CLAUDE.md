# What This Does

Dataset management utilities for uploading structured evaluation data to LangSmith, including movie rating examples and documentation for creating new datasets.

# File Structure

```
├── upload_dataset.py         # Script to upload datasets to LangSmith
├── movie_ratings_dataset.json # Sample dataset with movie rating examples
└── data-creation.md          # Guide for creating new datasets
```

# Quick Start

- Entry point: `upload_dataset.py` - uploads JSON data to LangSmith
- Run: `uv run upload_dataset.py` - creates and uploads dataset
- Test: Check LangSmith UI for uploaded datasets

# How It Works

The upload script reads JSON files containing evaluation examples, creates a named dataset in LangSmith, then bulk uploads all examples. Each example includes inputs and expected outputs for evaluation.

# Interfaces

```python
# Main usage pattern from upload_dataset.py
from langsmith import Client

client = Client()
dataset = client.create_dataset(
    dataset_name="Movie Ratings Dataset",
    description="Movie rating predictions..."
)

# Example dataset structure (from JSON):
examples = [
    {
        "inputs": {
            "movie_description": "A movie about...",
            "decade": "2000s"
        },
        "outputs": {
            "rating": "PG-13"
        }
    }
]

client.create_examples(dataset_id=dataset.id, examples=examples)
```

# Dependencies

- Reads data from: Local JSON files
- Uploads data to: LangSmith cloud storage
- Used by: Evaluation scripts in `/eval` and `/old-tests`

# Key Patterns

- JSON structure must have "inputs" and "outputs" keys
- Use absolute paths when loading JSON files
- Always provide dataset description for clarity

# Common Tasks

- Add new dataset: Create JSON file, modify upload script
- Update examples: Edit JSON, re-run upload script
- Debug uploads: Check return values and LangSmith UI

# Recent Updates

- Added movie ratings dataset with multiple examples
- Created upload utility with automatic path resolution
- Added data creation documentation guide

# Watch Out For

- Duplicate dataset names will create new versions
- Large datasets may take time to upload
- JSON must be valid - validate before uploading

Key Insights:

- Datasets are central to LangSmith evaluation workflows
- Structured format enables consistent testing across prompts