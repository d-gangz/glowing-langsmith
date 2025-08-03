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

## Project Structure

### Core Directories

- **`eval/`**: Evaluation scripts and demos

  - `movie_identifier_demo.py`: Demo using movie-identifier prompt from LangSmith
  - `evals.py`: Core evaluation utilities (in development)
  - `CLAUDE.md`: Evaluation-specific documentation

- **`dataset/`**: Dataset management and examples

  - `movie_ratings_dataset.json`: Sample dataset for movie rating classification
  - `upload_dataset.py`: Script to upload datasets to LangSmith
  - `CLAUDE.md`: Dataset creation and management guide

- **`old-tests/`**: Legacy experimental scripts
  - `eval-prompt.py`, `prompt-stream.py`, `prompt-test.py`, `prompt-so.py`

### Documentation

- **`ls-mcp-learnings.md`**: Comprehensive LangSmith MCP tools documentation
- **`langsmith-learnings.md`**: General LangSmith learning notes

## Code Architecture

### Key Dependencies

- **langsmith**: Core client for LangSmith API interactions
- **langchain-core, langchain-openai, langchain-google-genai**: LLM integration layers
- **python-dotenv**: Environment variable management

### Script Patterns

The codebase follows these patterns for LangSmith interactions:

1. **Basic Evaluation** (`old-tests/eval-prompt.py`):

   - Pull stored prompts with `client.pull_prompt()`
   - Create evaluation functions that invoke prompts
   - Run evaluations with `client.evaluate()`

2. **Streaming Evaluation** (`old-tests/prompt-stream.py`):

   - Use async functions for streaming responses
   - Measure time-to-first-token metrics
   - Handle chunks with `prompt.astream()`
   - Run async evaluations with `client.aevaluate()`

3. **Dataset Management** (`dataset/upload_dataset.py`):

   - Create datasets with structured examples
   - Upload to LangSmith for evaluation
   - Include metadata for filtering and analysis

4. **Demo Applications** (`eval/movie_identifier_demo.py`):
   - Pull prompts with model settings included
   - Use prompts directly as chains
   - Process multiple examples with evaluation

### Important Notes

- All scripts log interactions to LangSmith for analysis
- Streaming evaluation provides better performance metrics than non-streaming
- The `old-tests/` directory contains experimental code that may be refactored
- New evaluation work should be done in the `eval/` directory
- Dataset examples and uploads are managed in the `dataset/` directory

## LangSmith MCP Server Usage

When using the LangSmith MCP server tools, refer to `ls-mcp-learnings.md` for comprehensive documentation on:

- Available MCP tools and their exact names
- Parameter types (especially boolean parameters as strings)
- Detailed usage examples and workflows
- Best practices for prompt management, run analysis, and dataset operations

## Recent Updates (Updated: 2025-08-03)

### Major Changes

- **Project Reorganization**: Moved old experimental scripts to `old-tests/` directory
- **New Evaluation Framework**: Added `eval/` directory with movie identifier demo
- **Dataset Management**: Added `dataset/` directory with upload utilities and examples
- **Enhanced Documentation**: Added comprehensive MCP tools guide (`ls-mcp-learnings.md`)
- **Code Quality**: Improved formatting and client initialization patterns

### New Features

- Movie rating classification dataset and evaluation demo
- LangSmith MCP integration with detailed tool documentation
- Structured dataset upload utilities
- Improved prompt management with model settings inclusion

### File Organization

- Consolidated experimental code in `old-tests/`
- Created focused directories for evaluation (`eval/`) and datasets (`dataset/`)
- Added directory-specific documentation files
