<!--
Document Type: Guide
Purpose: Comprehensive guide for setting up LangSmith projects with proper dev/prod separation
Context: Research findings on LangSmith best practices for evaluation software architecture
Key Topics: Environment separation, project structure, configuration management, evaluation workflows
Target Use: Reference guide for implementing LangSmith in multi-environment setups
-->

# LangSmith Project Structure Guide: Development to Production

## Table of Contents

1. [Overview](#overview)
2. [Core Principles](#core-principles)
3. [Environment Configuration](#environment-configuration)
4. [Project Structure](#project-structure)
5. [Resource Management](#resource-management)
6. [Evaluation Workflows](#evaluation-workflows)
7. [Dataset Management](#dataset-management)
8. [Code Organization](#code-organization)
9. [CI/CD Integration](#cicd-integration)
10. [Production Monitoring](#production-monitoring)
11. [Migration Strategy](#migration-strategy)
12. [References](#references)

## Overview

LangSmith is a unified platform for debugging, testing, evaluating, and monitoring LLM applications throughout their lifecycle. This guide provides comprehensive recommendations for structuring LangSmith projects to effectively separate development and production environments while maintaining code reusability and operational efficiency.

## Core Principles

### 1. Use Resource Tags for Environment Separation

**Important**: Do not use Workspaces for environment separation as you cannot share resources across Workspaces[^1]. Instead, use resource tags with the default tag key `Environment` and different values (e.g., `dev`, `staging`, `prod`).

This approach enables:

- Resource sharing across environments
- Fine-grained access control when ABAC (Attribute-Based Access Control) is released
- Better organization of tracing projects

### 2. Project-Based Organization

Applications should be organized under projects, with each environment having its own project name[^2]. Projects are the primary organizational unit in LangSmith where all runs are logged.

## Environment Configuration

### Basic Environment Variables

LangSmith requires the following environment variables[^3][^4]:

```bash
# Required
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=<YOUR-LANGSMITH-API-KEY>

# Optional but recommended
LANGCHAIN_PROJECT=<YOUR-PROJECT-NAME>
```

### Environment-Specific Configuration Files

Create separate configuration files for each environment[^5]:

**.env.development**

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls__dev_xxxxxx
LANGSMITH_PROJECT=my-app-development
LANGSMITH_ENDPOINT=https://api.smith.langchain.com/
LANGSMITH_VERBOSE=true  # More verbose logging for dev
```

**.env.staging**

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls__staging_xxxxxx
LANGSMITH_PROJECT=my-app-staging
LANGSMITH_ENDPOINT=https://api.smith.langchain.com/
LANGSMITH_VERBOSE=false
```

**.env.production**

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls__prod_xxxxxx
LANGSMITH_PROJECT=my-app-production
LANGSMITH_ENDPOINT=https://api.smith.langchain.com/
LANGSMITH_VERBOSE=false
```

## Project Structure

### Recommended Directory Layout

```
my-app/
├── .env.development
├── .env.staging
├── .env.production
├── langsmith/
│   ├── datasets/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   ├── evaluators/
│   │   ├── custom/
│   │   └── shared/
│   └── experiments/
├── src/
│   └── langsmith_config.py
└── tests/
    └── evaluations/
```

## Resource Management

### Tagging Strategy

Tags can be used to filter workspace-scoped resources including Projects, Datasets, Annotation Queues, Deployments, and Experiments[^1]. Each workspace comes with two default tag keys:

- **Application**: Tag resources by application name
- **Environment**: Tag resources by environment (dev, staging, prod)

Example tagging structure:

```python
tags = {
    "environment": "production",
    "application": "chatbot",
    "version": "1.2.3",
    "feature_flags": "rag_enabled"
}
```

## Evaluation Workflows

### Development to Production Pipeline

LangSmith supports both offline and online evaluation workflows[^6]:

1. **Development Phase**: Offline Evaluation

   - Test on reference datasets
   - Rapid iteration with small datasets (10-50 examples)
   - Experiment with prompts and models

2. **Staging Phase**: Regression Testing

   - Compare against baseline performance
   - Test with larger datasets (100-1000 examples)
   - Validate before production deployment

3. **Production Phase**: Online Evaluation
   - Monitor real traffic with sampling
   - Set up automated alerts
   - Continuous quality monitoring

### Offline Evaluation (Pre-deployment)

Offline evaluation tests your application on pre-compiled datasets before deployment[^6]. This can be done:

- Client-side using LangSmith SDK (Python/TypeScript)
- Server-side via Prompt Playground
- Through automated CI/CD pipelines

### Online Evaluation (Production)

Online evaluation monitors deployed applications on real traffic in near real-time[^6]. This is configured using Rule Automations with:

- Custom filters for specific traces
- Sampling rates to control evaluation volume
- Automated alerting for quality degradation

## Dataset Management

### Dataset Creation Methods

LangSmith offers multiple methods for dataset creation[^7]:

1. **From Production Traces**: Convert notable traces into dataset examples
2. **Manual Creation**: Through UI or programmatically via SDK
3. **Import**: From CSV or JSONL files
4. **Backtesting**: Use recent production runs for model comparison

### Dataset Naming Convention

```
{environment}-{purpose}-{version}

Examples:
- dev-chatbot-intents-v1
- staging-regression-tests-v2
- prod-user-feedback-v3
```

### Dataset Splits

Divide datasets into training, validation, and test sets to prevent overfitting[^8]. This follows standard machine learning workflows and enables better model evaluation.

## Code Organization

### Configuration Management

Create a centralized configuration module:

```python
# langsmith_config.py
import os
from enum import Enum
from typing import Dict, Any

class Environment(Enum):
    DEV = "development"
    STAGING = "staging"
    PROD = "production"

def get_langsmith_config(env: Environment) -> Dict[str, Any]:
    """Load environment-specific LangSmith configuration"""
    env_file = f".env.{env.value}"

    return {
        "tracing": os.getenv("LANGSMITH_TRACING", "true"),
        "api_key": os.getenv("LANGSMITH_API_KEY"),
        "project": os.getenv("LANGSMITH_PROJECT"),
        "endpoint": os.getenv("LANGSMITH_ENDPOINT"),
        "tags": {
            "environment": env.value,
            "application": os.getenv("APP_NAME", "my-app"),
            "version": os.getenv("APP_VERSION", "0.0.0")
        }
    }
```

### Decorator Usage

Use appropriate decorators for tracing[^2]:

- `@traceable` for generic functions
- `@chain` for LangChain runnables

Include project metadata when running evaluations:

```python
project_metadata = {
    "env": "testing-notebook",
    "model": "gpt-3.5-turbo",
    "prompt_version": "v2.1",
    "experiment_type": "regression"
}
```

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/langsmith-eval.yml
name: LangSmith Evaluation
on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install langsmith langchain

      - name: Run Offline Evaluation
        env:
          LANGSMITH_API_KEY: ${{ secrets.LANGSMITH_DEV_API_KEY }}
          LANGSMITH_PROJECT: my-app-ci-${{ github.run_number }}
        run: |
          python -m langsmith evaluate \
            --dataset dev-regression-tests-v1 \
            --evaluators accuracy relevance \
            --max-concurrency 5
```

## Production Monitoring

### Setting Up Automated Monitoring

Configure online evaluation rules for production[^9]:

```python
from langsmith import Client

client = Client()

# Create automation rule for production monitoring
rule = client.create_automation_rule(
    name="production-quality-monitoring",
    filter={
        "project": "my-app-production",
        "tags.environment": "production"
    },
    sampling_rate=0.1,  # Sample 10% of production traffic
    evaluators=["relevance", "harmfulness", "latency"],
    alert_thresholds={
        "relevance": 0.8,
        "harmfulness": 0.1,
        "latency_p95": 2000  # milliseconds
    },
    notification_channels=["email", "slack"]
)
```

### Key Metrics to Monitor

1. **Performance Metrics**:

   - Latency (p50, p95, p99)
   - Token usage and costs
   - Error rates

2. **Quality Metrics**:

   - Relevance scores
   - Harmfulness detection
   - Custom business metrics

3. **Operational Metrics**:
   - Request volume
   - Unique users
   - Feature adoption

## Migration Strategy

### For Existing Projects

1. **Phase 1: Add Environment Tags**

   - Tag existing resources with environment labels
   - Update tracing configuration to include tags

2. **Phase 2: Create Environment Projects**

   - Set up separate projects for dev/staging/prod
   - Configure environment-specific API keys

3. **Phase 3: Migrate Datasets**

   - Export existing datasets
   - Reorganize with naming conventions
   - Import to appropriate environments

4. **Phase 4: Implement CI/CD**

   - Add offline evaluation to build pipeline
   - Set up regression testing for staging

5. **Phase 5: Enable Production Monitoring**
   - Configure online evaluation rules
   - Set up alerting and dashboards
   - Implement human-in-the-loop feedback

## References

[^1]: [LangSmith Concepts - Resource Organization](https://docs.smith.langchain.com/administration/concepts) - Official documentation on workspace organization and resource tagging
[^2]: [LangSmith Web Search Results](https://www.langchain.com/langsmith) - General LangSmith platform information and best practices
[^3]: [LangSmith Walkthrough](https://python.langchain.com/v0.1/docs/langsmith/walkthrough/) - Python SDK walkthrough with environment setup
[^4]: [Get started with LangSmith](https://docs.smith.langchain.com/) - Official getting started guide with configuration examples
[^5]: [Log traces to specific project](https://docs.smith.langchain.com/observability/how_to_guides/log_traces_to_project) - Documentation on project-specific logging
[^6]: [Evaluation concepts](https://docs.smith.langchain.com/evaluation/concepts) - Comprehensive guide to offline and online evaluation
[^7]: [Creating and Managing Datasets in the UI](https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_in_application) - Dataset management documentation
[^8]: [Evaluation how-to guides](https://docs.smith.langchain.com/evaluation/how_to_guides) - Collection of evaluation best practices
[^9]: [An Introduction to Debugging And Testing LLMs in LangSmith](https://www.datacamp.com/tutorial/introduction-to-langsmith) - Third-party tutorial with practical examples

### Additional Resources

- [GitHub: langchain-ai/helm](https://github.com/langchain-ai/helm) - Official Helm charts for Kubernetes deployment
- [GitHub: langchain-ai/intro-to-langsmith](https://github.com/langchain-ai/intro-to-langsmith) - Tutorial repository with examples
- [Self-hosting LangSmith](https://docs.smith.langchain.com/self_hosting) - Documentation for enterprise self-hosting options
- [LangSmith API Reference](https://api.smith.langchain.com/redoc) - Complete API documentation
