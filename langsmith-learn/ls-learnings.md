<!--
Document Type: Learning Notes
Purpose: Consolidated technical findings and insights from working with LangSmith APIs and advanced features
Context: Research and experimentation findings on LangSmith implementation challenges and solutions
Key Topics: Environment configuration, API limitations, cross-project tracing, replicas functionality, troubleshooting
Target Use: Reference guide for understanding LangSmith capabilities, limitations, and correct implementation patterns
-->

# LangSmith Learnings: Technical Insights and Implementation Guide

## Table of Contents

1. [Overview](#overview)
2. [Environment Configuration](#environment-configuration)
3. [API Key Types](#api-key-types)
4. [Cross-Project Tracing with Replicas](#cross-project-tracing-with-replicas)
5. [Common Issues and Solutions](#common-issues-and-solutions)
6. [Best Practices](#best-practices)
7. [References](#references)

## Overview

This document consolidates key learnings and insights from working with LangSmith, including advanced tracing features, API limitations, and implementation challenges discovered through research and experimentation.

## Environment Configuration

### API Endpoint Configuration

**Critical Learning**: LangSmith requires proper regional endpoint configuration to avoid authentication failures<sup>[[4]](https://docs.smith.langchain.com/)</sup>.

- **Issue**: Without correct endpoint configuration, API calls may fail with 403 Forbidden errors
- **Solution**: Set the appropriate regional endpoint in your environment:

```bash
# For EU region
LANGCHAIN_ENDPOINT=https://eu.api.smith.langchain.com

# For US region (default)  
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### Required Environment Variables

LangSmith requires specific environment variables for proper operation<sup>[[4]](https://docs.smith.langchain.com/)</sup><sup>[[5]](https://python.langchain.com/v0.1/docs/langsmith/walkthrough/)</sup>:

```bash
# Essential variables
LANGCHAIN_TRACING_V2=true                    # Enables tracing functionality
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com  # Regional API endpoint  
LANGCHAIN_API_KEY=<YOUR-LANGSMITH-API-KEY>   # Authentication
LANGCHAIN_PROJECT=<YOUR-PROJECT-NAME>        # Default project for traces
```

**Important**: The `LANGCHAIN_TRACING_V2` environment variable must be set to `"true"` for the `@traceable` decorator to function<sup>[[1]](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.traceable)</sup>.

## API Key Types

LangSmith provides different API key types for different use cases:

- **Personal Access Token**: For individual user authentication (local development)
- **Service Key**: For automated systems and CI/CD workflows

## Cross-Project Tracing with Replicas

### Overview and Problem Statement

A common requirement in LangSmith implementations is to trace main agents in one project while simultaneously logging sub-agent executions to separate projects. This enables both orchestration view (main project) and isolated sub-agent performance analysis (separate projects).

**Common Misconception**: Using `@traceable(replicas=[{"project_name": "B"}])` on sub-agent functions.

**Reality**: The `@traceable` decorator does **not** have a `replicas` parameter<sup>[[1]](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.traceable)</sup>. This approach will cause runtime errors.

### Understanding the `replicas` Parameter

The `replicas` parameter allows sending run data to multiple destinations simultaneously<sup>[[2]](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.tracing_context)</sup>. It accepts a sequence of `WriteReplica` dictionaries that can include:

```python
replicas = [
    {"project_name": "target_project", "updates": {...}},
    {"api_url": "https://api.example.com", "api_key": "key", "project_name": "external_proj"}
]
```

**Key Capabilities**:
- Cross-project trace replication within the same LangSmith instance
- Cross-instance replication to external LangSmith deployments  
- Selective data updates during replication

### Where `replicas` Actually Exists

Based on official LangSmith documentation research, the `replicas` parameter is available in:

#### ✅ `tracing_context()` Context Manager
```python
from langsmith import tracing_context

with tracing_context(replicas=[{"project_name": "B"}]):
    # Traces within this context are replicated to project B
    sub_agent_function()
```

#### ✅ `RunTree` Constructor
```python
from langsmith import RunTree

with RunTree(name="sub_agent", replicas=[{"project_name": "B"}]) as run:
    # This run and its children are replicated to project B
    result = sub_agent_logic()
```

#### ❌ `@traceable` Decorator
The `@traceable` decorator parameters include `run_type`, `name`, `metadata`, `tags`, `client`, and `project_name`, but **not** `replicas`<sup>[[1]](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.traceable)</sup>.

### Correct Implementation Methods

#### Method 1: Using `tracing_context` with `@traceable`

```python
from langsmith import traceable, tracing_context

@traceable(project_name="A")
def main_agent():
    """Main agent traced to Project A"""
    sub_agent_1()
    sub_agent_2()

@traceable()
def sub_agent_1():
    """Sub-agent replicated to Project B while maintaining Project A hierarchy"""
    with tracing_context(replicas=[{"project_name": "B"}]):
        # Sub-agent logic here
        return process_sub_task()

@traceable()  
def sub_agent_2():
    """Another sub-agent with different replica configuration"""
    with tracing_context(replicas=[{"project_name": "C"}]):
        return process_other_task()
```

**Result**:
- **Project A**: Complete trace tree (main_agent → sub_agent_1, sub_agent_2)
- **Project B**: Separate root trace for sub_agent_1 execution only
- **Project C**: Separate root trace for sub_agent_2 execution only

#### Method 2: Using `RunTree` Directly

```python
from langsmith import RunTree

def main_agent():
    """Manual trace management with precise replica control"""
    with RunTree(name="main_agent", project_name="A") as parent_run:
        
        # Create replicated child run
        with parent_run.create_child(
            name="sub_agent_1",
            replicas=[{"project_name": "B"}]
        ) as child_run:
            result = sub_agent_logic()
            child_run.outputs = {"result": result}
            
        return {"status": "completed"}
```

#### Method 3: Hybrid Approach with Conditional Replication

```python
from langsmith import traceable, tracing_context
import os

@traceable(project_name="A")
def main_agent(enable_sub_agent_tracking: bool = False):
    """Main agent with optional sub-agent replication"""
    result_1 = sub_agent_with_optional_replication("task_1", enable_sub_agent_tracking)
    result_2 = sub_agent_with_optional_replication("task_2", enable_sub_agent_tracking)
    return {"results": [result_1, result_2]}

@traceable()
def sub_agent_with_optional_replication(task: str, enable_replication: bool):
    """Sub-agent with conditional replication based on environment/configuration"""
    if enable_replication:
        with tracing_context(replicas=[{"project_name": "B"}]):
            return process_task(task)
    else:
        return process_task(task)
```

### Limitations and Current State

#### API Availability
- **tracing_context**: Fully documented and available<sup>[[2]](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.tracing_context)</sup>
- **RunTree**: Available with replicas parameter<sup>[[3]](https://docs.smith.langchain.com/reference/python/run_trees/langsmith.run_trees.RunTree)</sup>
- **@traceable**: No replicas support in current implementation

#### Trace Hierarchy Behavior
- **Within Project A**: Full parent-child hierarchy maintained
- **In Replica Projects**: Sub-agent traces appear as **root traces only**
- **No Cross-Project Parent Context**: Replica projects cannot show parent context from origin project

This means you cannot have a trace tree that spans multiple projects - replication creates independent root traces in target projects.

### Best Practices for Multi-Project Tracing

#### 1. Clear Project Naming Conventions
```python
# Recommended naming pattern
main_project = "hotel-agent-prod-orchestrator"
sub_projects = {
    "housekeeping": "hotel-agent-prod-housekeeping", 
    "maintenance": "hotel-agent-prod-maintenance",
    "front-desk": "hotel-agent-prod-front-desk"
}
```

#### 2. Consistent Metadata for Correlation
```python
@traceable(metadata={"trace_id": "unique_trace_id", "session_id": "session_123"})
def main_agent():
    with tracing_context(
        replicas=[{"project_name": "B"}],
        metadata={"main_trace_id": "unique_trace_id", "correlation_id": "corr_456"}
    ):
        sub_agent_function()
```

#### 3. Environment-Specific Replication
```python
def get_replica_config(environment: str) -> list:
    """Environment-specific replica configuration"""
    if environment == "production":
        return [{"project_name": f"hotel-agent-{environment}-sub-agents"}]
    elif environment == "development":
        return []  # No replication in dev
    else:
        return [{"project_name": f"hotel-agent-{environment}-experimental"}]
```

#### 4. Error Handling and Fallbacks
```python
@traceable()
def safe_sub_agent_with_replication(task: str):
    """Sub-agent with safe replication handling"""
    try:
        with tracing_context(replicas=[{"project_name": "B"}]):
            return process_task(task)
    except Exception as e:
        # Log error but don't fail the main operation
        logger.warning(f"Replication failed: {e}")
        return process_task(task)  # Continue without replication
```

This approach ensures your desired workflow: main agent orchestration visibility in Project A, with individual sub-agent performance tracking in dedicated projects.

## Common Issues and Solutions

### Authentication and Access Issues

#### 403 Forbidden Errors
**Common Causes**:
- Incorrect regional endpoint configuration
- Invalid or expired API key
- Insufficient account permissions
- Workspace/plan limitations

**Resolution Steps**:
1. Verify correct regional endpoint in `LANGCHAIN_ENDPOINT`
2. Validate API key format and permissions
3. Check workspace access and plan limitations
4. Ensure account has required feature access

#### Tracing Not Working
**Issue**: `@traceable` decorator has no effect on function execution<sup>[[6]](https://github.com/langchain-ai/langsmith-sdk/issues/1549)</sup>.

**Root Cause**: The `@traceable` decorator requires `LANGCHAIN_TRACING_V2=true` to be set in environment variables<sup>[[1]](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.traceable)</sup>.

**Solution**:
```bash
export LANGCHAIN_TRACING_V2=true
export LANGSMITH_API_KEY=your_api_key_here
```

### Cross-Project Tracing Issues

#### Replicas Parameter Not Found Error
**Issue**: `TypeError: traceable() got an unexpected keyword argument 'replicas'`

**Cause**: Attempting to use `@traceable(replicas=...)` which doesn't exist in the API.

**Solution**: Use `tracing_context` or `RunTree` as documented in the [Cross-Project Tracing](#cross-project-tracing-with-replicas) section.

#### Missing Parent-Child Relationships  
**Issue**: Sub-agent traces appear disconnected from main agent in replica projects.

**Expected Behavior**: This is by design. Replica projects show replicated runs as **root traces only**, without parent context from the original project<sup>[[2]](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.tracing_context)</sup>.

### Dataset and Resource Management

#### Dataset Creation Limitations
**Issue**: Dataset operations fail on free tier accounts.

**Cause**: Some LangSmith features require paid plans for full functionality.

**Solutions**:
- Verify plan limitations and feature availability
- Consider upgrading for advanced dataset operations
- Use smaller datasets within free tier limits

#### Resource Tagging Not Available
**Issue**: Cannot find resource tagging options in LangSmith UI.

**Causes**: 
- Resource tags require Plus or Enterprise plans
- Feature was released in August 2024
- Limited programmatic API support currently available

**Workarounds**:
- Use UI-based tag management for now
- Plan tag structure for future programmatic support
- Consider project naming conventions as alternative organization method

## Best Practices

### Environment and Configuration
1. **Always use environment variables for sensitive data**: Store API keys and configuration in environment files, never hardcode them<sup>[[4]](https://docs.smith.langchain.com/)</sup>
2. **Set correct regional endpoints**: Configure `LANGCHAIN_ENDPOINT` based on your account's region to avoid authentication failures
3. **Enable tracing early**: Set `LANGCHAIN_TRACING_V2=true` during development to ensure the `@traceable` decorator functions properly<sup>[[1]](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.traceable)</sup>
4. **Test API connectivity first**: Validate basic LangSmith operations before implementing complex tracing or evaluation workflows

### Cross-Project Tracing Implementation
5. **Use `tracing_context` for replicas**: Never attempt `@traceable(replicas=...)` - use the `tracing_context` context manager instead<sup>[[2]](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.tracing_context)</sup>
6. **Plan project hierarchy carefully**: Design project naming conventions early, considering both main orchestration and sub-agent isolation needs
7. **Include correlation metadata**: Add consistent metadata across related traces to enable correlation between main and replica projects
8. **Handle replication failures gracefully**: Implement error handling for replication operations to avoid impacting core application functionality

### Advanced Tracing Strategies  
9. **Understand replica limitations**: Remember that replica projects show root traces only, without parent context from origin projects
10. **Use conditional replication**: Implement environment-specific replication logic (e.g., only replicate in production)
11. **Consider RunTree for complex scenarios**: Use `RunTree` directly when you need precise control over trace hierarchy and replication timing
12. **Document cross-project relationships**: Maintain clear documentation of which traces appear in which projects to aid debugging and analysis

### Resource and Project Management
13. **Follow consistent naming conventions**: Use predictable patterns like `{app}-{env}-{component}` for project names
14. **Leverage resource tags when available**: Use UI-based resource tagging to organize projects, datasets, and prompts by environment and team
15. **Monitor API evolution**: Stay updated on LangSmith SDK releases for enhanced programmatic resource management capabilities
16. **Plan for scale**: Design your tracing architecture to accommodate growing numbers of agents, environments, and use cases

## References

[1]: [LangSmith @traceable Decorator Reference](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.traceable) - Official documentation for the @traceable decorator, including all supported parameters and usage requirements

[2]: [LangSmith tracing_context Reference](https://docs.smith.langchain.com/reference/python/run_helpers/langsmith.run_helpers.tracing_context) - Official documentation for the tracing_context context manager, including replicas parameter and cross-project tracing functionality

[3]: [LangSmith RunTree Reference](https://docs.smith.langchain.com/reference/python/run_trees/langsmith.run_trees.RunTree) - Official documentation for the RunTree class, including constructor parameters and replica support

[4]: [Get started with LangSmith](https://docs.smith.langchain.com/) - Official getting started guide with environment configuration and setup instructions

[5]: [LangSmith Walkthrough](https://python.langchain.com/v0.1/docs/langsmith/walkthrough/) - Comprehensive Python SDK walkthrough covering environment setup and basic usage patterns

[6]: [GitHub Issue: @traceable decorator enabling](https://github.com/langchain-ai/langsmith-sdk/issues/1549) - Community discussion on common tracing issues and solutions, including environment variable requirements
