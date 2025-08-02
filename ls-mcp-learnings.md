# LangSmith MCP Tools Guide

A comprehensive guide to using LangSmith MCP (Model Context Protocol) tools for prompt management, run analysis, and dataset operations.

## Available MCP Tools

The exact tool names as they appear in the MCP configuration:
- `mcp__LangSmith_MCP__list_prompts`
- `mcp__LangSmith_MCP__get_prompt_by_name`
- `mcp__LangSmith_MCP__get_thread_history`
- `mcp__LangSmith_MCP__get_project_runs_stats`
- `mcp__LangSmith_MCP__fetch_trace`
- `mcp__LangSmith_MCP__list_datasets`
- `mcp__LangSmith_MCP__list_examples`
- `mcp__LangSmith_MCP__read_dataset`
- `mcp__LangSmith_MCP__read_example`

## Important Notes on Parameter Types

**Boolean Parameters**: All boolean parameters in the LangSmith MCP tools are passed as strings:
- Use `"true"` (not `true`) for true values
- Use `"false"` (not `false`) for false values

This applies to parameters like `is_public`, `is_last_run`, etc.

## Table of Contents
1. [Prompt Management Tools](#1-prompt-management-tools)
2. [Conversation & Run Analysis Tools](#2-conversation--run-analysis-tools)
3. [Dataset & Evaluation Tools](#3-dataset--evaluation-tools)
4. [Practical Examples & Workflows](#4-practical-examples--workflows)
5. [Key Benefits](#key-benefits)

## 1. Prompt Management Tools

### `list_prompts`
**MCP Tool Name**: `mcp__LangSmith_MCP__list_prompts`
**Purpose**: Fetch prompts from LangSmith with optional filtering

**Parameters**:
- `is_public` (str): Filter by prompt visibility - "true" for public prompts, "false" for private prompts (default: "false")
- `limit` (int): Maximum number of prompts to return (default: 20)

**Returns**:
- `prompts`: Array of prompt objects containing:
  - `repo_handle`: The prompt's handle/identifier
  - `description`: Prompt description
  - `id`: Unique prompt ID
  - `is_public`: Boolean visibility status
  - `tags`: Array of tags (e.g., ["ChatPromptTemplate"])
  - `owner`: Owner information
  - `full_name`: Full name of the prompt
  - `num_likes`: Number of likes
  - `num_downloads`: Download count
  - `num_views`: View count
  - `created_at`: ISO timestamp of creation
  - `updated_at`: ISO timestamp of last update
- `total_count`: Total number of prompts matching the filter

**Example Usage**:
```json
// List all your private prompts
Tool: mcp__LangSmith_MCP__list_prompts
Parameters: {
  "is_public": "false",
  "limit": 20
}

// List public prompts
Tool: mcp__LangSmith_MCP__list_prompts
Parameters: {
  "is_public": "true",
  "limit": 50
}
```

**Use Cases**: 
- Inventory your prompt library
- Find prompts by creation date
- See download/view statistics
- Track prompt popularity

### `get_prompt_by_name`
**MCP Tool Name**: `mcp__LangSmith_MCP__get_prompt_by_name`
**Purpose**: Get a specific prompt by its exact name

**Parameters**:
- `prompt_name` (str): The exact name of the prompt to retrieve (required)

**Returns**:
- Dictionary containing the prompt details and template, including:
  - Full prompt object with model/tool bindings
  - String representation of the complete prompt configuration
  - Template content and variables
  - Model settings and configurations
- Or an error message if the prompt cannot be found

**Example Usage**:
```json
// Get a prompt by exact name
Tool: mcp__LangSmith_MCP__get_prompt_by_name
Parameters: {
  "prompt_name": "movie-identifier"
}

// Returns: Full prompt object including tools and config
```

**Use Cases**:
- Inspect prompt configuration
- View the actual prompt template
- Check model settings and tool bindings
- Debug prompt behavior
- Export prompt for local use

## 2. Conversation & Run Analysis Tools

### `get_thread_history`
**MCP Tool Name**: `mcp__LangSmith_MCP__get_thread_history`
**Purpose**: Retrieve the message history for a specific conversation thread

**Parameters**:
- `thread_id` (str): The unique ID of the thread to fetch history for (required)
- `project_name` (str): The name of the project containing the thread (format: "owner/project" or just "project") (required)

**Returns**:
- `result`: Array of messages from the thread, extracted from the most recent LLM run
  - Each message contains role, content, and other message properties
  - Messages include both input messages and output responses
- Or an error message if the thread cannot be found

**Example Usage**:
```json
// Get messages from a thread
Tool: mcp__LangSmith_MCP__get_thread_history
Parameters: {
  "thread_id": "abc-123-def",
  "project_name": "my-chatbot"
}

// Returns: Array of messages from the conversation
```

**Use Cases**:
- Debug conversation flows
- Analyze user interactions
- Extract conversation patterns
- Build conversation datasets
- Review chat history for quality assurance

### `get_project_runs_stats`
**MCP Tool Name**: `mcp__LangSmith_MCP__get_project_runs_stats`
**Purpose**: Get statistics about runs in a LangSmith project

**Parameters**:
- `project_name` (str): The name of the project to analyze (format: "owner/project" or just "project") (required)
- `is_last_run` (str): Set to "true" to get only the last run's stats, set to "false" for overall project stats (default: "true")

**Returns**:
- Dictionary containing the requested project run statistics:
  - When `is_last_run` is "true": Last run details including inputs, outputs, timestamps, model info
  - When `is_last_run` is "false": Aggregate statistics with run counts, latency percentiles, costs, error rates
  - Includes `project_name` field with the actual project name
- Or an error message if statistics cannot be retrieved

**Example Usage**:
```json
// Overall project statistics
Tool: mcp__LangSmith_MCP__get_project_runs_stats
Parameters: {
  "project_name": "default",
  "is_last_run": "false"
}

// Just the last run's stats
Tool: mcp__LangSmith_MCP__get_project_runs_stats
Parameters: {
  "project_name": "default",
  "is_last_run": "true"
}
```

**Use Cases**:
- Monitor latency (p50, p99)
- Track token usage and costs
- Check error rates
- Analyze streaming performance
- Set up performance alerts
- Review last run details for debugging

### `fetch_trace`
**MCP Tool Name**: `mcp__LangSmith_MCP__fetch_trace`
**Purpose**: Fetch trace content for debugging and analyzing LangSmith runs

**Parameters**:
- `project_name` (str, optional): The name of the project to fetch the latest trace from
- `trace_id` (str, optional): The specific ID of the trace to fetch (preferred parameter)

**Note**: Only one parameter (project_name or trace_id) is required. If both are provided, trace_id is preferred. String "null" inputs are handled as None values.

**Returns**:
- Dictionary containing the trace data and metadata:
  - `trace_id`: The trace ID
  - `run_type`: Type of run (e.g., "chain", "llm")
  - `inputs`: Input data to the run
  - `outputs`: Output data from the run
- Or an error message if the trace cannot be found

**Example Usage**:
```json
// Get latest trace from a project
Tool: mcp__LangSmith_MCP__fetch_trace
Parameters: {
  "project_name": "my-project"
}

// Get specific trace by ID
Tool: mcp__LangSmith_MCP__fetch_trace
Parameters: {
  "trace_id": "4d53c5d7-c818-4012-aa3c-597032979a0b"
}
```

**Use Cases**:
- Debug specific runs
- Inspect inputs/outputs
- Analyze token usage
- Review model responses
- Troubleshoot errors
- Open trace view in LangSmith UI

## 3. Dataset & Evaluation Tools

### `list_datasets`
**MCP Tool Name**: `mcp__LangSmith_MCP__list_datasets`
**Purpose**: Fetch LangSmith datasets

**Note**: If no arguments are provided, all datasets will be returned.

**Parameters**:
- `dataset_ids` (Optional[List[str]]): List of dataset IDs to filter by
- `data_type` (Optional[str]): Filter by dataset data type (e.g., 'chat', 'kv')
- `dataset_name` (Optional[str]): Filter by exact dataset name
- `dataset_name_contains` (Optional[str]): Filter by substring in dataset name
- `metadata` (Optional[Dict[str, Any]]): Filter by metadata dict
- `limit` (int): Max number of datasets to return (default: 20)

**Returns**:
- Dictionary containing the datasets and metadata:
  - `datasets`: Array of dataset objects with:
    - `id`: Dataset UUID
    - `name`: Dataset name
    - `inputs_schema_definition`: Input schema
    - `outputs_schema_definition`: Output schema
    - `description`: Dataset description
    - `data_type`: Type of data (e.g., 'kv', 'chat')
    - `example_count`: Number of examples
    - `session_count`: Number of sessions
    - `created_at`: ISO timestamp of creation
    - `modified_at`: ISO timestamp of last modification
    - `last_session_start_time`: Last session timestamp
  - `total_count`: Total number of datasets returned
- Or an error message if the datasets cannot be retrieved

**Example Usage**:
```json
// List all datasets
Tool: mcp__LangSmith_MCP__list_datasets
Parameters: {
  "limit": 20
}

// Filter by type
Tool: mcp__LangSmith_MCP__list_datasets
Parameters: {
  "data_type": "chat"
}

// Search by name
Tool: mcp__LangSmith_MCP__list_datasets
Parameters: {
  "dataset_name_contains": "movie"
}

// Filter by metadata
Tool: mcp__LangSmith_MCP__list_datasets
Parameters: {
  "metadata": {"tag": "production"}
}
```

**Use Cases**:
- Find datasets for evaluation
- Organize datasets by type
- Track dataset versions
- Manage test suites

### `read_dataset`
**MCP Tool Name**: `mcp__LangSmith_MCP__read_dataset`
**Purpose**: Read a specific dataset from LangSmith

**Note**: Either dataset_id or dataset_name must be provided to identify the dataset. If both are provided, dataset_id takes precedence.

**Parameters**:
- `dataset_id` (Optional[str]): Dataset ID to retrieve
- `dataset_name` (Optional[str]): Dataset name to retrieve

**Returns**:
- Dictionary containing the dataset details:
  - `dataset`: Dataset object with:
    - `id`: Dataset UUID (as string)
    - `name`: Dataset name
    - `inputs_schema_definition`: Input schema
    - `outputs_schema_definition`: Output schema
    - `description`: Dataset description
    - `data_type`: Type of data
    - `example_count`: Number of examples
    - `session_count`: Number of sessions
    - `created_at`: ISO timestamp of creation
    - `modified_at`: ISO timestamp of last modification
    - `last_session_start_time`: Last session timestamp
- Or an error message if the dataset cannot be retrieved

**Example Usage**:
```json
// By ID
Tool: mcp__LangSmith_MCP__read_dataset
Parameters: {
  "dataset_id": "e9f950eb-1fd7-4f4f-97a9-a6db6e7e7a84"
}

// By name
Tool: mcp__LangSmith_MCP__read_dataset
Parameters: {
  "dataset_name": "Movie Ratings Dataset"
}
```

**Use Cases**:
- Check dataset metadata
- View example count
- Inspect schema definitions
- Verify dataset integrity

### `list_examples`
**MCP Tool Name**: `mcp__LangSmith_MCP__list_examples`
**Purpose**: Fetch examples from a LangSmith dataset with advanced filtering options

**Note**: Either dataset_id, dataset_name, or example_ids must be provided. If multiple are provided, they are used in order of precedence: example_ids, dataset_id, dataset_name.

**Parameters**:
- `dataset_id` (Optional[str]): Dataset ID to retrieve examples from
- `dataset_name` (Optional[str]): Dataset name to retrieve examples from
- `example_ids` (Optional[List[str]]): List of specific example IDs to retrieve
- `limit` (Optional[int]): Maximum number of examples to return
- `offset` (Optional[int]): Number of examples to skip before starting to return results
- `filter` (Optional[str]): Filter string using LangSmith query syntax (e.g., 'has(metadata, {"key": "value"})')
- `metadata` (Optional[Dict[str, Any]]): Dictionary of metadata to filter by
- `splits` (Optional[List[str]]): List of dataset splits to include examples from
- `inline_s3_urls` (Optional[bool]): Whether to inline S3 URLs (default: SDK default if not specified)
- `include_attachments` (Optional[bool]): Whether to include attachments in response (default: SDK default if not specified)
- `as_of` (Optional[str]): Dataset version tag OR ISO timestamp to retrieve examples as of that version/time

**Returns**:
- Dictionary containing the examples and metadata:
  - `examples`: Array of example objects with:
    - `id`: Example UUID (as string)
    - `dataset_id`: Dataset UUID (as string)
    - `inputs`: Input data for the example
    - `outputs`: Expected output data
    - `metadata`: Example metadata
    - `created_at`: ISO timestamp of creation
    - `modified_at`: ISO timestamp of last modification
    - `runs`: Associated run information
    - `source_run_id`: Source run UUID (as string)
    - `attachments`: Any attachments
  - `total_count`: Total number of examples returned
- Or an error message if the examples cannot be retrieved

**Example Usage**:
```json
// Basic listing
Tool: mcp__LangSmith_MCP__list_examples
Parameters: {
  "dataset_name": "Movie Ratings Dataset"
}

// With filtering
Tool: mcp__LangSmith_MCP__list_examples
Parameters: {
  "dataset_id": "abc-123",
  "filter": "has(metadata, {\"difficulty\": \"hard\"})",
  "splits": ["test"],
  "limit": 10
}

// Get specific examples
Tool: mcp__LangSmith_MCP__list_examples
Parameters: {
  "example_ids": ["id1", "id2", "id3"]
}

// Pagination
Tool: mcp__LangSmith_MCP__list_examples
Parameters: {
  "dataset_name": "Large Dataset",
  "limit": 50,
  "offset": 50
}
```

**Use Cases**:
- Build evaluation sets
- Export training data
- Analyze example distribution
- Create data subsets

### `read_example`
**MCP Tool Name**: `mcp__LangSmith_MCP__read_example`
**Purpose**: Read a specific example from LangSmith

**Parameters**:
- `example_id` (str): Example ID to retrieve (required)
- `as_of` (Optional[str]): Dataset version tag OR ISO timestamp to retrieve the example as of that version/time

**Returns**:
- Dictionary containing the example details:
  - `example`: Example object with:
    - `id`: Example UUID (as string)
    - `dataset_id`: Dataset UUID (as string)
    - `inputs`: Input data for the example
    - `outputs`: Expected output data
    - `metadata`: Example metadata
    - `created_at`: ISO timestamp of creation
    - `modified_at`: ISO timestamp of last modification
    - `runs`: Associated run information
    - `source_run_id`: Source run UUID (as string)
    - `attachments`: Any attachments
- Or an error message if the example cannot be retrieved

**Example Usage**:
```json
// Read current version
Tool: mcp__LangSmith_MCP__read_example
Parameters: {
  "example_id": "50d357d7-80a3-482b-b0b0-d8375db7b941"
}

// Read historical version
Tool: mcp__LangSmith_MCP__read_example
Parameters: {
  "example_id": "50d357d7-80a3-482b-b0b0-d8375db7b941",
  "as_of": "2024-01-01T00:00:00Z"
}
```

**Use Cases**:
- Inspect individual test cases
- Track example changes over time
- Debug evaluation failures
- Audit data quality

## 4. Practical Examples & Workflows

### Example 1: Prompt Version Management
```json
// Step 1: List all your prompts
Tool: mcp__LangSmith_MCP__list_prompts
Parameters: {
  "is_public": "false",
  "limit": 100
}

// Returns: List of prompts with stats like:
// - repo_handle, num_downloads, num_views
// - created_at, updated_at

// Step 2: Get details of a specific prompt
Tool: mcp__LangSmith_MCP__get_prompt_by_name
Parameters: {
  "prompt_name": "movie-identifier"
}

// Returns: Full prompt template and configuration
```

### Example 2: Performance Monitoring Dashboard
```json
// Step 1: Get project performance metrics
Tool: mcp__LangSmith_MCP__get_project_runs_stats
Parameters: {
  "project_name": "my-chatbot",
  "is_last_run": "false"
}

// Returns metrics including:
// - run_count: 28
// - error_rate: 0.0
// - latency_p50: 0.6405
// - latency_p99: 6.48793
// - total_cost: 0.0004168
// - streaming_rate: 0.0

// Step 2: If latency is high, investigate with trace
Tool: mcp__LangSmith_MCP__fetch_trace
Parameters: {
  "project_name": "my-chatbot"
}

// Returns detailed trace with inputs, outputs, model info
```

### Example 3: Dataset Evaluation Pipeline
```json
// Step 1: Find datasets containing "test"
Tool: mcp__LangSmith_MCP__list_datasets
Parameters: {
  "dataset_name_contains": "test"
}

// Step 2: Get dataset details
Tool: mcp__LangSmith_MCP__read_dataset
Parameters: {
  "dataset_name": "Movie Ratings Dataset"
}

// Returns: name, example_count, description, etc.

// Step 3: Filter examples by difficulty
Tool: mcp__LangSmith_MCP__list_examples
Parameters: {
  "dataset_id": "e9f950eb-1fd7-4f4f-97a9-a6db6e7e7a84",
  "filter": "has(metadata, {\"difficulty\": \"easy\"})",
  "limit": 10
}

// Step 4: Get all examples to analyze distribution
Tool: mcp__LangSmith_MCP__list_examples
Parameters: {
  "dataset_id": "e9f950eb-1fd7-4f4f-97a9-a6db6e7e7a84",
  "limit": 100
}
```

### Example 4: Debugging Failed Runs
```json
// Step 1: Check project health
Tool: mcp__LangSmith_MCP__get_project_runs_stats
Parameters: {
  "project_name": "production-app",
  "is_last_run": "false"
}

// If error_rate > 0, investigate:

// Step 2: Get the latest trace
Tool: mcp__LangSmith_MCP__fetch_trace
Parameters: {
  "project_name": "production-app"
}

// Returns trace with:
// - trace_id: "4d53c5d7-c818-4012-aa3c-597032979a0b"
// - inputs: {"movie_description": "...", "decade": "..."}
// - outputs: Including error details or token usage
// - response_metadata: Model info, token counts
```

### Example 5: Building a Test Suite
```json
// Step 1: Find testing datasets
Tool: mcp__LangSmith_MCP__list_datasets
Parameters: {
  "metadata": {"purpose": "testing"}
}

// Step 2: For each dataset, get test examples
Tool: mcp__LangSmith_MCP__list_examples
Parameters: {
  "dataset_id": "dataset-id-here",
  "splits": ["test"],
  "limit": 5
}

// Step 3: Get specific example details
Tool: mcp__LangSmith_MCP__read_example
Parameters: {
  "example_id": "50d357d7-80a3-482b-b0b0-d8375db7b941"
}

// Returns complete example with:
// - inputs, outputs (expected results)
// - metadata (difficulty, tags, etc.)
// - created_at, modified_at timestamps
```

## Key Benefits

### Prompt Tools Benefits
- **Version Control**: Track prompt changes over time
- **Usage Analytics**: Monitor which prompts are most effective
- **Collaboration**: Share prompts across teams
- **A/B Testing**: Compare prompt performance

### Run Analysis Tools Benefits
- **Performance Monitoring**: Track latency, errors, and costs in real-time
- **Cost Tracking**: Monitor and optimize LLM spending
- **Debugging**: Deep dive into specific runs to fix issues
- **Quality Assurance**: Ensure consistent model behavior

### Dataset Tools Benefits
- **Systematic Evaluation**: Run consistent tests across model versions
- **Test Case Management**: Organize and version your test data
- **Quality Assurance**: Ensure model outputs meet expectations
- **Regression Testing**: Catch performance degradations early

## Best Practices

1. **Regular Monitoring**: Set up automated checks using `get_project_runs_stats`
2. **Version Everything**: Use dataset versioning and prompt versioning
3. **Filter Efficiently**: Use metadata and filters to work with relevant data subsets
4. **Batch Operations**: Process multiple examples/runs together for efficiency
5. **Error Handling**: Always handle potential API errors gracefully

These tools essentially give you programmatic access to most of LangSmith's UI features, enabling automation, monitoring, and integration into your development workflow.