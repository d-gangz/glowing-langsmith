# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangSmith experimentation sandbox for exploring and testing LangSmith features including:

- Prompt management and versioning
- Dataset creation and evaluation
- Performance tracking with streaming metrics
- LLM interaction logging and tracing

## Development Commands

### Environment Setup

```bash
# Install dependencies using UV (preferred)
uv pip install -r requirements.txt

# Or with standard pip
pip install -r requirements.txt

# Update requirements.txt after installing new packages
uv pip freeze > requirements.txt
```

### Code Quality Tools

```bash
# Format code
black .

# Lint code
pylint *.py old-tests/*.py

# Type checking
mypy . --ignore-missing-imports
```

### Running Scripts

Run all scripts using `uv run`

## Code Architecture

### Key Dependencies

- **langsmith**: Core client for LangSmith API interactions
- **langchain-core, langchain-openai, langchain-google-genai**: LLM integration layers
- **python-dotenv**: Environment variable management

### Script Patterns

The codebase follows these patterns for LangSmith interactions:

1. **Basic Evaluation** (`eval-prompt.py`):

   - Pull stored prompts with `client.pull_prompt()`
   - Create evaluation functions that invoke prompts
   - Run evaluations with `client.evaluate()`

2. **Streaming Evaluation** (`prompt-stream.py`):
   - Use async functions for streaming responses
   - Measure time-to-first-token metrics
   - Handle chunks with `prompt.astream()`
   - Run async evaluations with `client.aevaluate()`

### Important Notes

- All scripts log interactions to LangSmith for analysis
- Streaming evaluation provides better performance metrics than non-streaming
- The `old-tests/` directory contains experimental code that may be refactored
