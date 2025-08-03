# What This Does

Legacy experimental scripts exploring different LangSmith features including prompt evaluation, streaming responses, and asynchronous testing patterns - kept for reference and learning.

# File Structure

```
├── eval-prompt.py    # Basic evaluation with story outline generator
├── prompt-stream.py  # Async streaming with time-to-first-token metrics
├── prompt-test.py    # Simple prompt testing and invocation
└── prompt-so.py      # Stack Overflow helper with traceable functions
```

# Quick Start

- Entry point: Any script can be run independently
- Run: `uv run eval-prompt.py` - evaluates story outlines
- Test: Scripts are self-contained experiments

# How It Works

Each script demonstrates a different LangSmith pattern: basic evaluation pulls prompts and runs them against datasets, streaming captures performance metrics, and traceable functions add custom observability.

# Interfaces

```python
# Basic evaluation pattern (eval-prompt.py)
prompt = client.pull_prompt("story-outline", include_model=True)
def target_function(inputs):
    return prompt.invoke(inputs)
client.evaluate(target_function, data="dataset-name")

# Streaming pattern (prompt-stream.py)
async def stream_prompt(inputs):
    first_token_time = None
    async for chunk in prompt.astream(inputs):
        if first_token_time is None:
            first_token_time = time.time()
    return {"time_to_first_token": first_token_time}

# Traceable pattern (prompt-so.py)
@traceable
def custom_function(query: str):
    # Function automatically traced in LangSmith
    return process_query(query)
```

# Dependencies

- Gets prompts from: LangSmith cloud
- Sends traces to: LangSmith for analysis
- Evolution path: These patterns moved to `/eval` directory

# Key Patterns

- Async functions for streaming evaluation
- Time-to-first-token metrics for performance
- @traceable decorator for custom observability

# Common Tasks

- Test new prompt: Modify prompt name in pull_prompt()
- Add metrics: Extend evaluation functions with timing
- Debug streaming: Add print statements in async loops

# Recent Updates

- Moved to old-tests/ during project reorganization
- Kept as reference for different evaluation patterns
- Superseded by cleaner implementations in /eval

# Watch Out For

- These are experimental scripts - may have rough edges
- Async code requires proper event loop handling
- Some patterns may be outdated - check /eval for latest

Key Insights:

- Shows evolution of LangSmith integration patterns
- Valuable for understanding streaming vs non-streaming trade-offs