# What This Does

Evaluation scripts for testing LangSmith prompts with real examples, including movie identification demos and core evaluation utilities for performance tracking.

# File Structure

```
├── movie_identifier_demo.py # Demo script using movie-identifier prompt from LangSmith
├── evals.py                 # Core evaluation utilities (empty - in development)
└── prompts-guide.md         # Documentation for prompt management
```

# Quick Start

- Entry point: `movie_identifier_demo.py` - runs movie identification examples
- Run: `uv run movie_identifier_demo.py` - identifies movies from descriptions
- Test: No tests yet - demos serve as validation

# How It Works

The demo pulls prompts from LangSmith with model settings included, then invokes them directly as chains. Results are automatically logged to LangSmith for analysis and performance tracking.

# Interfaces

```python
# Main usage pattern from movie_identifier_demo.py
from langsmith import Client

client = Client()
prompt = client.pull_prompt("movie-identifier", include_model=True)
chain = prompt  # Prompt already includes model when include_model=True

# Example usage:
result = chain.invoke({
    "movie_description": "A group of unlikely heroes...",
    "decade": "2000s"
})
```

# Dependencies

- Gets prompts from: LangSmith cloud (via API)
- Sends traces to: LangSmith for analysis
- Shares patterns with: `/old-tests` (similar evaluation approaches)

# Key Patterns

- Always use `include_model=True` when pulling prompts
- Prompts become directly invokable chains
- All invocations automatically traced to LangSmith

# Common Tasks

- Add new demo: Create script following `movie_identifier_demo.py` pattern
- Change prompt: Update prompt name in `client.pull_prompt()`
- Debug issues: Check LangSmith UI for trace details

# Recent Updates

- Added movie identifier demo with example movie descriptions
- Simplified client initialization (no explicit API key needed)
- Created placeholder for core evaluation utilities

# Watch Out For

- Ensure LANGSMITH_API_KEY is set in environment
- Prompts must exist in LangSmith before pulling
- Empty `evals.py` is placeholder for future utilities

Key Insights:

- This directory focuses on practical prompt evaluation examples
- Direct integration with LangSmith for prompt management and tracing