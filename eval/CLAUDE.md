# Using LangSmith Prompts - Quick Guide

## Getting Started

When you copy a prompt from LangSmith UI, you'll get code like this:
```python
# Create a LANGSMITH_API_KEY in Settings > API Keys
from langsmith import Client
client = Client(api_key=LANGSMITH_API_KEY)
prompt = client.pull_prompt("movie-identifier", include_model=True)
```

## Key Concepts

### 1. The `include_model` Parameter

- **`include_model=True`**: Returns a complete chain (prompt + model) ready to use
- **`include_model=False`** (default): Returns only the prompt template

```python
# With include_model=True - ready to use
chain = client.pull_prompt("movie-identifier", include_model=True)
result = chain.invoke({"movie_description": "...", "decade": "..."})
print(result.content)  # AI response

# Without include_model - need to add model
prompt = client.pull_prompt("movie-identifier")
# Just returns formatted messages, not AI response
```

### 2. Complete Working Example

```python
import os
from langsmith import Client
from dotenv import load_dotenv

# Setup
load_dotenv()
client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))

# Pull prompt with model
chain = client.pull_prompt("movie-identifier", include_model=True)

# Use it
result = chain.invoke({
    "movie_description": "A shark terrorizes a beach town",
    "decade": "1970s"
})

print(result.content)  # Output: {"movie_title": "Jaws", ...}
```

### 3. Important Notes

1. **Environment Variables**: Always set BOTH:
   - `LANGSMITH_API_KEY` - Required to pull prompts from LangSmith
   - `OPENAI_API_KEY` (or other model API keys) - Still required even with `include_model=True`!
   
   **Why?** When using `include_model=True`, you don't need to import `ChatOpenAI`, but the chain internally creates a model instance that needs the API key to make actual calls.

2. **Input Variables**: Must match exactly what the prompt expects
   ```python
   # Check expected variables first
   prompt = client.pull_prompt("my-prompt")
   print(prompt.input_variables)  # ['var1', 'var2']
   ```

3. **Batch Processing**: Process multiple inputs efficiently
   ```python
   results = chain.batch([
       {"movie_description": "...", "decade": "..."},
       {"movie_description": "...", "decade": "..."}
   ])
   ```

4. **Version Control**: Pull specific versions if needed
   ```python
   # Latest version
   prompt = client.pull_prompt("movie-identifier")
   
   # Specific version
   prompt = client.pull_prompt("movie-identifier:commit_hash")
   ```

### 4. Common Patterns

```python
# Basic invocation
result = chain.invoke({"key": "value"})

# With error handling
try:
    result = chain.invoke({"key": "value"})
    print(result.content)
except Exception as e:
    print(f"Error: {e}")

# Async for better performance
async def process():
    result = await chain.ainvoke({"key": "value"})
    return result
```

## Quick Checklist

- [ ] Set environment variables (`LANGSMITH_API_KEY`, `OPENAI_API_KEY`, etc.)
  - Even with `include_model=True`, you still need the model's API key!
- [ ] Use `include_model=True` for ready-to-use chains
- [ ] Match input dictionary keys to prompt variables exactly
- [ ] Handle errors appropriately
- [ ] Use `.content` to access the AI response text