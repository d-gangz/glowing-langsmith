# What This Does

Prompt testing and demo scripts for LangSmith integration, including movie identification examples and GPT-5 model testing with the responses API for advanced reasoning capabilities.

# File Structure

```
├── gpt-5-test.py            # GPT-5 testing with responses API and reasoning settings
├── movie_identifier_demo.py # Demo script using movie-identifier prompt from LangSmith
└── prompts-guide.md         # Documentation for prompt management
```

# Quick Start

## Movie Identification Demo
- Entry point: `movie_identifier_demo.py` - runs movie identification examples
- Run: `uv run movie_identifier_demo.py` - identifies movies from descriptions

## GPT-5 Testing Demo
- Entry point: `gpt-5-test.py` - tests GPT-5 with responses API
- Run: `uv run gpt-5-test.py` - demonstrates reasoning capabilities with story analysis
- Test: No tests yet - demos serve as validation

# How It Works

## Movie Identifier Demo
Pulls prompts from LangSmith with model settings included, then invokes them directly as chains. Results are automatically logged to LangSmith for analysis and performance tracking.

## GPT-5 Test Demo
Uses the OpenAI responses API with GPT-5 to enable chain of thought reasoning across messages. Configures reasoning effort levels and text verbosity for different use cases.

# Interfaces

## Movie Identifier Pattern
```python
from langsmith import Client

client = Client()
prompt = client.pull_prompt("movie-identifier", include_model=True)
chain = prompt  # Prompt already includes model when include_model=True

result = chain.invoke({
    "movie_description": "A group of unlikely heroes...",
    "decade": "2000s"
})
```

## GPT-5 Responses API Pattern
```python
from langchain_openai import ChatOpenAI
from langsmith import Client

client = Client()
prompt = client.pull_prompt("gpt5-test")

model = ChatOpenAI(
    model="gpt-5",
    output_version="responses/v1",
    reasoning={"effort": "minimal"},  # "minimal", "medium", "high"
    model_kwargs={"text": {"verbosity": "high"}},  # "low", "medium", "high"
)

chain = prompt | model
result = chain.invoke({"story": "Your story description here"})
```

# Dependencies

- Gets prompts from: LangSmith cloud (via API)
- Sends traces to: LangSmith for analysis
- Shares patterns with: `/old-tests` (similar evaluation approaches)

# Key Patterns

## Movie Identifier
- Always use `include_model=True` when pulling prompts
- Prompts become directly invokable chains
- All invocations automatically traced to LangSmith

## GPT-5 Testing  
- Use `output_version="responses/v1"` for responses API
- Configure `reasoning` effort: "minimal", "medium", or "high"
- Set text `verbosity` in model_kwargs: "low", "medium", or "high"
- Chain prompts with models using `|` operator

# Common Tasks

- Add new movie demo: Create script following `movie_identifier_demo.py` pattern
- Add GPT-5 demo: Create script following `gpt-5-test.py` pattern 
- Change prompt: Update prompt name in `client.pull_prompt()`
- Adjust GPT-5 reasoning: Modify `reasoning` effort or text `verbosity` settings
- Debug issues: Check LangSmith UI for trace details

# Recent Updates

- Added GPT-5 test demo with responses API integration
- Configured reasoning effort and text verbosity settings for GPT-5
- Added movie identifier demo with example movie descriptions
- Simplified client initialization (no explicit API key needed)
- Removed evals.py placeholder - core utilities moved to `/eval` directory

# Watch Out For

- Ensure LANGSMITH_API_KEY is set in environment
- Prompts must exist in LangSmith before pulling (e.g., "movie-identifier", "gpt5-test")
- GPT-5 requires access to OpenAI's responses API
- Reasoning settings only work with `output_version="responses/v1"`

Key Insights:

- This directory focuses on practical prompt testing and advanced model integration
- Direct integration with LangSmith for prompt management and tracing
- Demonstrates both traditional prompting and advanced GPT-5 reasoning capabilities