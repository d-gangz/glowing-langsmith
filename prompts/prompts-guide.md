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

### 5. Using LangChain's ChatOpenAI Directly

When you want more control over model configuration, you can use LangChain's ChatOpenAI directly:

```python
from langchain_openai import ChatOpenAI
from langsmith import Client

# Pull just the prompt (without model)
client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
prompt = client.pull_prompt("movie-identifier")

# Create your own model with custom settings
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    model_kwargs={"response_format": {"type": "text"}}  # Custom model arguments
)

# Combine prompt + model
chain = prompt | model
result = chain.invoke({"movie_description": "...", "decade": "..."})
```

**Important Note for Structured Output**: When using structured output features, you **cannot** use `model_kwargs`. The structured output functionality conflicts with custom model arguments.

```python
# ❌ This will cause an error with structured output
model = ChatOpenAI(
    model="gpt-4o",
    model_kwargs={"response_format": {"type": "json_object"}}
)

# ✅ For structured output, remove model_kwargs entirely
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7
    # No model_kwargs when using structured output
)

# Then use structured output methods
from pydantic import BaseModel

class MovieResponse(BaseModel):
    movie_title: str
    confidence: float

structured_model = model.with_structured_output(MovieResponse)
chain = prompt | structured_model
```

### 6. GPT-5 Verbosity + Structured Output: LangChain Limitation

**Key Finding**: OpenAI's API **does support** both verbosity and structured output together, but LangChain's current implementation doesn't handle this correctly.

**The Problem**: LangChain's `.with_structured_output()` uses the older Chat Completions API's `response_format` parameter, which conflicts with `model_kwargs`. However, OpenAI's newer Responses API supports both features simultaneously via the `text.format` structure.

**Evidence from OpenAI API**:
```python
# This works in raw OpenAI API
"sampling_params": {
    "text": {
        "verbosity": "high",        # ✅ Verbosity control
        "format": {                 # ✅ Structured output  
            "type": "json_schema",
            "name": "movie_analysis",
            "schema": {...},
            "strict": True
        }
    }
}
```

**Workaround - Use Raw OpenAI Client**:
```python
import openai
from pydantic import BaseModel, Field

class MovieAnalysis(BaseModel):
    response: str = Field(description="Analysis of the movie")
    genre: str = Field(description="Primary genre")

# Convert Pydantic to JSON schema
schema = MovieAnalysis.model_json_schema()

# Use raw OpenAI client with Responses API
client = openai.OpenAI()
response = client.responses.create(
    model="gpt-5",
    input="Analyze this story: A group of heroes...",
    reasoning={"effort": "minimal"},
    text={
        "verbosity": "high",  # ✅ Works together
        "format": {           # ✅ Works together
            "type": "json_schema",
            "name": "movie_analysis", 
            "schema": schema,
            "strict": True
        }
    }
)

# Get structured output with verbosity
result = response.output_parsed  # Already a MovieAnalysis object
```

**Status**: This is a LangChain implementation gap, not an OpenAI API limitation. LangChain will likely need to update their ChatOpenAI class to properly support GPT-5's Responses API structure.

## Quick Checklist

- [ ] Set environment variables (`LANGSMITH_API_KEY`, `OPENAI_API_KEY`, etc.)
  - Even with `include_model=True`, you still need the model's API key!
- [ ] Use `include_model=True` for ready-to-use chains
- [ ] Match input dictionary keys to prompt variables exactly
- [ ] Handle errors appropriately
- [ ] Use `.content` to access the AI response text
- [ ] Remove `model_kwargs` when using structured output features with LangChain
- [ ] For GPT-5 verbosity + structured output, use raw OpenAI client until LangChain updates