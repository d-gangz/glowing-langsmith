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
3. [Organizational Hierarchy and Access Control](#organizational-hierarchy-and-access-control)
4. [Environment Configuration](#environment-configuration)
5. [Project Structure](#project-structure)
6. [Resource Management](#resource-management)
7. [Resource Tagging Strategies](#resource-tagging-strategies)
8. [Evaluation Workflows](#evaluation-workflows)
9. [Dataset Management](#dataset-management)
10. [Dynamic Project Logging](#dynamic-project-logging)
11. [Code Organization](#code-organization)
12. [CI/CD Integration](#cicd-integration)
13. [Production Monitoring](#production-monitoring)
14. [Migration Strategy](#migration-strategy)
15. [Troubleshooting](#troubleshooting)
16. [References](#references)

## Overview

LangSmith is a unified platform for debugging, testing, evaluating, and monitoring LLM applications throughout their lifecycle. This guide provides comprehensive recommendations for structuring LangSmith projects to effectively separate development and production environments while maintaining code reusability and operational efficiency.

## Core Principles

### 1. Use Resource Tags for Environment Separation

**Important**: Do not use Workspaces for environment separation as you cannot share resources across Workspaces<sup>[[1]](https://docs.smith.langchain.com/administration/concepts)</sup>. Instead, use resource tags with the default tag key `Environment` and different values (e.g., `dev`, `staging`, `prod`).

This approach enables:

- Resource sharing across environments
- Fine-grained access control when ABAC (Attribute-Based Access Control) is released
- Better organization of tracing projects

### 2. Project-Based Organization

Applications should be organized under projects, with each environment having its own project name<sup>[[2]](https://www.langchain.com/langsmith)</sup>. Projects are the primary organizational unit in LangSmith where all runs are logged.

## Organizational Hierarchy and Access Control

### Understanding the LangSmith Hierarchy

LangSmith follows a three-tier organizational structure that determines access control, billing, and resource management<sup>[[10]](https://docs.smith.langchain.com/administration/concepts)</sup>:

```
Organization (Company Level)
├── Workspace A (Team/Department Level)
│   ├── Project 1 (Application/Environment Level)
│   ├── Dataset A
│   ├── Prompts Collection
│   └── Annotation Queue X
└── Workspace B (Team/Department Level)
    ├── Project 2
    ├── Dataset B
    └── Experiments Suite
```

### 1. Organizations (Top Level)

**Purpose**: Highest level grouping, typically one per company
**Contains**:
- Billing configuration and subscription management
- Multiple workspaces
- Organization-wide settings and policies

**When to Create**: 
- One organization per company/legal entity
- Separate organizations for completely isolated business units

### 2. Workspaces (Team Level)

**Purpose**: Logical grouping within organizations that provides **trust boundaries**
**Contains**:
- All LangSmith resources (Projects, Datasets, Prompts, etc.)
- Team-specific access controls
- Resource tags and organization

**When to Create New Workspaces**:
- ✅ **Different teams/departments** (e.g., "ML-Engineering", "Product-AI")
- ✅ **Different trust levels** (e.g., "Internal-Tools", "Customer-Facing")
- ✅ **Regulatory isolation** (e.g., "HIPAA-Compliant", "SOC2-Compliant")
- ✅ **Different security contexts** (e.g., "Public-Models", "Private-Models")

**When NOT to Create New Workspaces**:
- ❌ **Environment separation** (dev/staging/prod) - Use resource tags instead
- ❌ **Feature-based separation** - Use projects and tags instead
- ❌ **Temporary experiments** - Use projects with appropriate naming

### 3. Resources (Application Level)

**Workspace-scoped resources** include:
- **Projects**: Where traces and runs are logged
- **Datasets**: Evaluation and training data collections
- **Prompts**: Managed prompt templates and versions
- **Annotation Queues**: Human feedback collection
- **Deployments**: Model deployment tracking
- **Experiments**: Evaluation experiment results

### Access Control Best Practices

#### Team-Based Workspace Strategy
```
organization: "acme-corp"
├── workspace: "ml-platform-team"
│   ├── project: "ml-platform-dev"
│   ├── project: "ml-platform-staging" 
│   ├── project: "ml-platform-prod"
│   └── datasets: [training-data-v1, evaluation-benchmarks]
├── workspace: "product-ai-team"
│   ├── project: "recommendation-engine-dev"
│   ├── project: "recommendation-engine-prod"
│   └── datasets: [user-behavior-data, recommendation-eval]
└── workspace: "customer-support-ai"
    ├── project: "support-bot-dev"
    ├── project: "support-bot-prod" 
    └── datasets: [support-tickets, escalation-data]
```

#### Multi-Tenant Application Strategy
For applications serving multiple customers:

```
organization: "saas-provider"
├── workspace: "platform-engineering"
│   ├── project: "shared-infrastructure-dev"
│   ├── project: "shared-infrastructure-prod"
│   └── datasets: [platform-benchmarks, security-tests]
└── workspace: "customer-deployments"
    ├── project: "tenant-customerA-prod"
    ├── project: "tenant-customerB-prod"
    └── datasets: [tenant-specific-evaluations]
```

### Resource Sharing Limitations

**Cannot Share Across Workspaces**:
- Datasets cannot be shared between workspaces
- Prompts are workspace-scoped
- Projects cannot reference cross-workspace resources

**Can Share Within Workspaces**:
- Datasets can be used across multiple projects
- Prompts can be reused across projects
- Evaluation results can compare across projects

### Planning Your Workspace Strategy

#### Questions to Ask:
1. **Trust Boundaries**: Do these resources require the same level of access control?
2. **Team Ownership**: Will the same team manage these resources?
3. **Data Sharing**: Do these resources need to share datasets or prompts?
4. **Compliance**: Do different regulatory requirements apply?

#### Example: Hotel Agent System
For your multi-agent hotel system, consider:

```
organization: "hotel-management-corp"
├── workspace: "ai-platform-team"
│   ├── project: "hotel-agent-dev"
│   ├── project: "hotel-agent-staging"
│   ├── project: "hotel-agent-prod"
│   ├── datasets: [housekeeping-scenarios, maintenance-requests]
│   └── prompts: [orchestrator-prompts, department-specific-prompts]
└── workspace: "hotel-operations"  # If different team manages
    ├── project: "operations-analytics-dev"
    ├── project: "operations-analytics-prod" 
    └── datasets: [operational-metrics, customer-feedback]
```

**Key Insight**: Use resource tags within workspaces for environment separation (dev/staging/prod), not separate workspaces.

## Environment Configuration

### Basic Environment Variables

LangSmith requires the following environment variables<sup>[[3]](https://python.langchain.com/v0.1/docs/langsmith/walkthrough/)</sup><sup>[[4]](https://docs.smith.langchain.com/)</sup>:

```bash
# Required
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=<YOUR-LANGSMITH-API-KEY>

# Optional but recommended
LANGCHAIN_PROJECT=<YOUR-PROJECT-NAME>
```

### Environment-Specific Configuration Files

Create separate configuration files for each environment<sup>[[5]](https://docs.smith.langchain.com/observability/how_to_guides/log_traces_to_project)</sup>:

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

### Understanding LangSmith Resource Tags

LangSmith implements an AWS-style resource tagging system to help organize and manage resources within workspaces<sup>[[10]](https://docs.smith.langchain.com/administration/concepts)</sup>. Resource tags are key-value pairs that function similarly to tags in cloud services like AWS, Azure, or Google Cloud Platform.

#### Tag System Overview

**What are Resource Tags?**
- Key-value pairs attached to LangSmith resources
- Enable filtering, searching, and organizational grouping
- Follow AWS-style tagging conventions
- Workspace-scoped (cannot share across workspaces)

**Available Since**: August 2024 (relatively new feature)
**Plan Requirements**: Plus and Enterprise plans only
**Management**: Currently primarily UI-based (programmatic API limited)

#### Taggable Resources

Resource tags can be applied to these **workspace-scoped resources only**:
- ✅ **Projects** (Tracing projects where runs are logged)
- ✅ **Datasets** (Evaluation and training data collections)
- ✅ **Prompts** (Managed prompt templates and versions)
- ✅ **Annotation Queues** (Human feedback collection systems)
- ✅ **Deployments** (Model deployment tracking)
- ✅ **Experiments** (Evaluation experiment results)

#### Default Tag Keys

Each workspace comes with two pre-configured tag keys:
- **Application**: Tag resources by application or service name
- **Environment**: Tag resources by deployment environment (dev, staging, prod)

#### Current Limitations

**Programmatic Access**:
- ❌ **Limited SDK support**: No general resource tagging API methods available
- ❌ **No creation-time tagging**: Cannot set tags during resource creation via SDK
- ✅ **UI-based management**: Full tag management available through LangSmith UI
- ⚠️ **Dataset version tags**: Limited SDK support for dataset version tagging only

**Access and Scope**:
- ❌ **Workspace boundaries**: Cannot share tagged resources across workspaces
- ❌ **Free tier**: Resource tags require Plus or Enterprise plan
- ✅ **Within workspace**: Full filtering and organization capabilities

### Tagging Strategy Framework

#### AWS-Style Tagging Best Practices

Following cloud tagging conventions, structure your tags using these categories:

**1. Technical Tags**
```python
technical_tags = {
    "environment": "production",      # dev, staging, prod
    "application": "hotel-agent",     # application identifier
    "component": "housekeeping",      # service/component name
    "version": "v2.1.0",             # version identifier
}
```

**2. Business Tags**
```python
business_tags = {
    "owner": "ai-platform-team",      # team responsible
    "project": "q4-agent-rollout",    # business project
    "cost-center": "engineering",     # billing allocation
    "priority": "high",               # business priority
}
```

**3. Operational Tags**
```python
operational_tags = {
    "backup": "daily",                # backup requirements
    "monitoring": "enabled",          # monitoring status
    "compliance": "soc2",             # compliance requirements
    "lifecycle": "active",            # resource lifecycle stage
}
```

#### Environment Separation Pattern

**Recommended**: Use resource tags for environment separation within a workspace:

```python
# Development resources
dev_tags = {
    "environment": "development",
    "application": "hotel-agent",
    "component": "main-orchestrator",
    "team": "ai-platform"
}

# Staging resources  
staging_tags = {
    "environment": "staging",
    "application": "hotel-agent", 
    "component": "main-orchestrator",
    "team": "ai-platform"
}

# Production resources
prod_tags = {
    "environment": "production",
    "application": "hotel-agent",
    "component": "main-orchestrator", 
    "team": "ai-platform",
    "compliance": "required"
}
```

#### Multi-Agent System Tagging

For complex systems like your hotel agent architecture:

```python
# Main orchestrator
orchestrator_tags = {
    "environment": "production",
    "application": "hotel-agent",
    "component": "orchestrator",
    "agent-type": "main",
    "department": "all"
}

# Department-specific agents
housekeeping_tags = {
    "environment": "production", 
    "application": "hotel-agent",
    "component": "housekeeping-agent",
    "agent-type": "sub-agent",
    "department": "housekeeping"
}

maintenance_tags = {
    "environment": "production",
    "application": "hotel-agent", 
    "component": "maintenance-agent",
    "agent-type": "sub-agent",
    "department": "maintenance"
}
```

### Current Tag Management Methods

#### UI-Based Tag Management (Current Primary Method)

**Adding Tags to Resources**:
1. Navigate to resource detail page (Project, Dataset, etc.)
2. Click "Resource tags" button
3. Assign key-value pairs from available workspace tags
4. Save changes

**Managing Tag Keys and Values**:
1. Go to Workspace Settings
2. Navigate to Resource Tags section
3. Create/edit tag keys and their allowed values
4. Delete unused tags using trash icon

#### Limited Programmatic Support

**Dataset Version Tagging Only** (Available via SDK):
```python
from langsmith import Client

client = Client()

# Tag a specific version of a dataset (NOT general resource tagging)
client.update_dataset_tag(
    dataset_name="hotel-scenarios-v1",
    as_of=datetime(2024, 1, 1), 
    tag="prod"  # This is version labeling, not resource tagging
)
```

**Important Note**: This dataset version tagging is different from the resource tags discussed above and is used for dataset version management, not organizational resource tagging.

## Resource Tagging Strategies

### Tag Governance and Planning

Effective resource tagging requires upfront planning and consistent governance across your organization. This section outlines strategic approaches for implementing a robust tagging system.

#### Tag Taxonomy Design

**Hierarchical Tag Structure**:
Design your tag taxonomy to reflect your organizational structure and operational needs:

```
Level 1: Organization-wide standards
├── environment: [dev, staging, prod]
├── application: [hotel-agent, analytics-platform, customer-portal]
└── owner: [ai-platform-team, data-team, frontend-team]

Level 2: Application-specific tags  
├── component: [orchestrator, housekeeping-agent, maintenance-agent]
├── agent-type: [main, sub-agent, utility]
└── department: [housekeeping, maintenance, front-desk, concierge]

Level 3: Operational tags
├── priority: [low, medium, high, critical]  
├── lifecycle: [experimental, active, deprecated]
└── compliance: [none, soc2, hipaa, gdpr]
```

#### Tag Naming Conventions

**Consistent Naming Rules**:
- Use lowercase with hyphens: `hotel-agent` not `Hotel_Agent`
- Be descriptive but concise: `housekeeping-agent` not `hka`
- Use standard abbreviations: `prod` not `production-environment`
- Avoid spaces and special characters: `front-desk` not `front desk`

**Value Standards**:
```python
# Good: Consistent and predictable
environment_values = ["dev", "staging", "prod"]
priority_values = ["low", "medium", "high", "critical"]
agent_type_values = ["main", "sub-agent", "utility"]

# Avoid: Inconsistent variations
# ["development", "dev", "Development", "DEV"]
# ["Low", "MEDIUM", "high", "Hi"]
```

### Multi-Environment Tagging Strategies

#### Strategy 1: Environment-Centric Tagging

**Best for**: Traditional software development lifecycles with clear environment boundaries.

```python
# Development environment resources
dev_project_tags = {
    "environment": "dev",
    "application": "hotel-agent",
    "component": "orchestrator",
    "team": "ai-platform",
    "cost-center": "engineering",
    "data-classification": "test"
}

dev_dataset_tags = {
    "environment": "dev", 
    "application": "hotel-agent",
    "dataset-type": "training",
    "data-source": "synthetic",
    "retention": "30-days"
}

# Production environment resources
prod_project_tags = {
    "environment": "prod",
    "application": "hotel-agent", 
    "component": "orchestrator",
    "team": "ai-platform",
    "cost-center": "operations",
    "compliance": "soc2",
    "monitoring": "required",
    "backup": "daily"
}
```

#### Strategy 2: Feature-Branch Tagging

**Best for**: Rapid development with multiple feature branches and A/B testing.

```python
# Feature development
feature_tags = {
    "environment": "dev",
    "application": "hotel-agent",
    "feature-branch": "advanced-routing-v2",
    "experiment-id": "exp-routing-2024-q1",
    "temporary": "true",
    "auto-cleanup": "30-days"
}

# A/B testing variants
variant_a_tags = {
    "environment": "prod",
    "application": "hotel-agent",
    "experiment": "routing-algorithm-test", 
    "variant": "control",
    "traffic-split": "50-percent"
}

variant_b_tags = {
    "environment": "prod", 
    "application": "hotel-agent",
    "experiment": "routing-algorithm-test",
    "variant": "treatment", 
    "traffic-split": "50-percent"
}
```

### Multi-Tenant Application Tagging

For your hotel agent system serving multiple hotel chains or properties:

#### Strategy 1: Tenant Isolation

```python
# Hotel Chain A resources
chain_a_tags = {
    "environment": "prod",
    "application": "hotel-agent",
    "tenant": "marriott-international",
    "region": "north-america",
    "compliance": "ccpa",
    "data-residency": "us-west"
}

# Hotel Chain B resources  
chain_b_tags = {
    "environment": "prod",
    "application": "hotel-agent", 
    "tenant": "hilton-worldwide",
    "region": "europe",
    "compliance": "gdpr",
    "data-residency": "eu-west"
}
```

#### Strategy 2: Service-Based Tagging

```python
# Shared infrastructure
shared_infrastructure_tags = {
    "environment": "prod",
    "application": "hotel-agent",
    "component": "shared-orchestrator",
    "tenant": "multi-tenant",
    "scaling": "auto",
    "cost-allocation": "shared"
}

# Tenant-specific agents
tenant_specific_tags = {
    "environment": "prod",
    "application": "hotel-agent", 
    "component": "housekeeping-agent",
    "tenant": "marriott-international",
    "customization": "tenant-specific",
    "cost-allocation": "dedicated"
}
```

### Operational Tag Patterns

#### Resource Lifecycle Management

```python
# Development/experimental resources
experimental_tags = {
    "lifecycle": "experimental",
    "auto-cleanup": "7-days",
    "monitoring": "basic",
    "backup": "none"
}

# Production resources
production_tags = {
    "lifecycle": "production", 
    "auto-cleanup": "never",
    "monitoring": "comprehensive",
    "backup": "daily",
    "disaster-recovery": "required"
}

# Deprecated resources
deprecated_tags = {
    "lifecycle": "deprecated",
    "auto-cleanup": "30-days", 
    "monitoring": "alerts-only",
    "backup": "final-backup",
    "migration-target": "hotel-agent-v2"
}
```

#### Cost Management and Optimization

```python
# Cost allocation tags
cost_tags = {
    "cost-center": "engineering",
    "budget-category": "r-and-d",
    "project-code": "proj-2024-q1-agent",
    "billing-team": "ai-platform"
}

# Resource optimization hints
optimization_tags = {
    "usage-pattern": "business-hours",  
    "scaling-policy": "predictive",
    "cost-optimization": "enabled",
    "rightsizing": "monthly-review"
}
```

### Tag-Based Resource Queries and Filters

#### Common Query Patterns

Once programmatic API support becomes available, these patterns will be useful:

```python
# Conceptual examples for future API support

# Find all production resources for a specific application
production_resources = client.list_resources(
    tags={"environment": "prod", "application": "hotel-agent"}
)

# Find experimental resources for cleanup
experimental_resources = client.list_resources(
    tags={"lifecycle": "experimental", "auto-cleanup": "7-days"}
)

# Find all resources owned by a specific team
team_resources = client.list_resources(
    tags={"owner": "ai-platform-team"}
)

# Find tenant-specific resources
tenant_resources = client.list_resources(
    tags={"tenant": "marriott-international", "environment": "prod"}
)
```

#### Resource Organization Views

**By Environment**:
- dev: All development resources across applications
- staging: Pre-production validation resources  
- prod: Production resources with compliance requirements

**By Application**:
- hotel-agent: All resources related to the hotel agent system
- analytics-platform: Business intelligence and reporting resources
- customer-portal: Customer-facing application resources

**By Team/Ownership**:
- ai-platform-team: ML/AI resources and models
- data-team: Data pipelines and storage resources
- operations-team: Infrastructure and monitoring resources

### Future-Proofing Your Tagging Strategy

#### Preparing for Enhanced API Support

As LangSmith's resource tagging API matures, prepare by:

1. **Establish Tag Standards Now**: Define your taxonomy through UI management
2. **Document Tag Policies**: Create governance documentation for your team
3. **Plan Migration Scripts**: Prepare to bulk-update tags when API support arrives
4. **Monitor API Evolution**: Watch for SDK updates and new tagging capabilities

#### Integration with External Systems

Plan for future integration possibilities:
- **Cost Management**: Export tag data for cloud cost allocation
- **ITSM Integration**: Sync tags with service management platforms  
- **Security Compliance**: Automate compliance reporting based on tags
- **Resource Discovery**: Enable cross-platform resource inventory

## Evaluation Workflows

### Development to Production Pipeline

LangSmith supports both offline and online evaluation workflows<sup>[[6]](https://docs.smith.langchain.com/evaluation/concepts)</sup>:

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

Offline evaluation tests your application on pre-compiled datasets before deployment<sup>[[6]](https://docs.smith.langchain.com/evaluation/concepts)</sup>. This can be done:

- Client-side using LangSmith SDK (Python/TypeScript)
- Server-side via Prompt Playground
- Through automated CI/CD pipelines

### Online Evaluation (Production)

Online evaluation monitors deployed applications on real traffic in near real-time<sup>[[6]](https://docs.smith.langchain.com/evaluation/concepts)</sup>. This is configured using Rule Automations with:

- Custom filters for specific traces
- Sampling rates to control evaluation volume
- Automated alerting for quality degradation

## Dataset Management

### Dataset Creation Methods

LangSmith offers multiple methods for dataset creation<sup>[[7]](https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_in_application)</sup>:

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

Divide datasets into training, validation, and test sets to prevent overfitting<sup>[[8]](https://docs.smith.langchain.com/evaluation/how_to_guides)</sup>. This follows standard machine learning workflows and enables better model evaluation.

## Dynamic Project Logging

### Overview

Dynamic project logging allows you to log traces to different LangSmith projects at runtime, enabling you to use the same code base while organizing traces by different contexts, environments, or features<sup>[[5]](https://docs.smith.langchain.com/observability/how_to_guides/log_traces_to_project)</sup>. This is particularly valuable for multi-tenant applications, A/B testing, or when you need granular trace organization within a single application.

### Prerequisites

Ensure the following environment variable is set for tracing to work:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=your_api_key_here
```

### Method 1: Static Project Assignment with @traceable

Use the `project_name` parameter in the `@traceable` decorator to assign traces to specific projects:

```python
import openai
from langsmith import traceable

client = openai.Client()

@traceable(
    run_type="llm",
    name="User Authentication",
    project_name="auth-service-prod"
)
def authenticate_user(username: str, password: str) -> dict:
    """All authentication traces go to auth-service-prod project"""
    messages = [
        {"role": "system", "content": "You are a security validator."},
        {"role": "user", "content": f"Validate login attempt for {username}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    return {
        "username": username,
        "validation_result": response.choices[0].message.content,
        "project": "auth-service-prod"
    }

@traceable(
    run_type="llm", 
    name="Payment Processing",
    project_name="payments-service-prod"
)
def process_payment(amount: float, payment_method: str) -> dict:
    """All payment traces go to payments-service-prod project"""
    messages = [
        {"role": "system", "content": "You are a payment processor."},
        {"role": "user", "content": f"Process ${amount} payment via {payment_method}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    return {
        "amount": amount,
        "status": response.choices[0].message.content,
        "project": "payments-service-prod"
    }
```

### Method 2: Runtime Project Override with langsmith_extra

Override project assignment at call time using `langsmith_extra`:

```python
import openai
from langsmith import traceable
import os

client = openai.Client()

@traceable(
    run_type="llm",
    name="Multi-Environment Handler",
    project_name="default-project"  # This gets overridden
)
def handle_request(request_type: str, environment: str, data: dict) -> str:
    """Same function, different projects based on environment"""
    messages = [
        {"role": "system", "content": f"You are handling {request_type} requests."},
        {"role": "user", "content": f"Process this data: {data}"}
    ]
    
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    ).choices[0].message.content

# Usage examples - same function, different projects
# Development traces
dev_result = handle_request(
    "support_ticket", 
    "dev", 
    {"ticket_id": "123", "issue": "login problem"},
    langsmith_extra={"project_name": "support-service-dev"}
)

# Production traces  
prod_result = handle_request(
    "support_ticket",
    "prod", 
    {"ticket_id": "456", "issue": "payment failed"},
    langsmith_extra={"project_name": "support-service-prod"}
)

# A/B testing traces
ab_test_result = handle_request(
    "recommendation",
    "prod",
    {"user_id": "789", "preferences": ["tech", "books"]},
    langsmith_extra={"project_name": "recommendation-ab-test-v2"}
)
```

### Method 3: Dynamic Project Names with Lambda Functions

Create project names dynamically based on input parameters:

```python
import openai
from langsmith import traceable
from datetime import datetime

client = openai.Client()

# Project name determined by tenant ID
@traceable(
    run_type="llm",
    name="Tenant Request Handler", 
    project_name=lambda tenant_id, *args: f"tenant-{tenant_id}-requests"
)
def handle_tenant_request(tenant_id: str, request: str) -> dict:
    """Routes traces to tenant-specific projects"""
    messages = [
        {"role": "system", "content": f"You are handling requests for tenant {tenant_id}."},
        {"role": "user", "content": request}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    return {
        "tenant_id": tenant_id,
        "response": response.choices[0].message.content,
        "project": f"tenant-{tenant_id}-requests"
    }

# Project name with environment and feature context
@traceable(
    run_type="llm",
    name="Feature Flag Handler",
    project_name=lambda env, feature, *args: f"{env}-feature-{feature}"
)
def handle_with_features(env: str, feature: str, user_query: str) -> str:
    """Routes traces based on environment and active features"""
    messages = [
        {"role": "system", "content": f"Feature {feature} is enabled in {env}."},
        {"role": "user", "content": user_query}
    ]
    
    return client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages
    ).choices[0].message.content

# Usage examples
tenant_result = handle_tenant_request("acme-corp", "How do I reset my password?")
# Logs to: "tenant-acme-corp-requests"

feature_result = handle_with_features("prod", "advanced-search", "Find all invoices from last month")
# Logs to: "prod-feature-advanced-search"
```

### Method 4: Wrapped OpenAI Client with Dynamic Projects

Use LangSmith's OpenAI wrapper for automatic tracing with dynamic projects:

```python
import openai
from langsmith import wrappers

# Create wrapped client
client = openai.Client()
wrapped_client = wrappers.wrap_openai(client)

def customer_service_bot(department: str, customer_tier: str, query: str) -> str:
    """Route customer service traces to department and tier specific projects"""
    
    project_name = f"customer-service-{department}-{customer_tier}"
    
    messages = [
        {"role": "system", "content": f"You are a {department} specialist for {customer_tier} customers."},
        {"role": "user", "content": query}
    ]
    
    response = wrapped_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        langsmith_extra={"project_name": project_name}
    )
    
    return response.choices[0].message.content

# Usage examples
support_response = customer_service_bot(
    "technical-support", 
    "premium", 
    "My API calls are failing with 500 errors"
)
# Logs to: "customer-service-technical-support-premium"

billing_response = customer_service_bot(
    "billing", 
    "basic", 
    "I was charged twice this month"
)
# Logs to: "customer-service-billing-basic"
```

### Method 5: RunTree for Advanced Project Control

Use RunTree for maximum control over project assignment and trace metadata:

```python
import openai
from langsmith.run_trees import RunTree
import uuid
from datetime import datetime

client = openai.Client()

def advanced_request_handler(context: dict, user_input: str) -> dict:
    """Advanced handler with full trace customization"""
    
    # Determine project name from context
    environment = context.get("environment", "dev")
    service = context.get("service", "general")
    user_tier = context.get("user_tier", "basic")
    
    project_name = f"{environment}-{service}-{user_tier}"
    
    # Create RunTree with detailed configuration
    rt = RunTree(
        run_type="llm",
        name="Advanced Request Processing",
        inputs={
            "user_input": user_input,
            "context": context
        },
        project_name=project_name,
        tags=[
            f"env:{environment}",
            f"service:{service}", 
            f"tier:{user_tier}",
            f"timestamp:{datetime.now().strftime('%Y-%m-%d')}"
        ],
        metadata={
            "session_id": context.get("session_id", str(uuid.uuid4())),
            "user_id": context.get("user_id"),
            "feature_flags": context.get("feature_flags", []),
            "request_timestamp": datetime.now().isoformat()
        }
    )
    
    try:
        # Execute the LLM call
        messages = [
            {"role": "system", "content": f"You are a {service} assistant for {user_tier} users."},
            {"role": "user", "content": user_input}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        result = {
            "response": response.choices[0].message.content,
            "project": project_name,
            "tokens_used": response.usage.total_tokens,
            "model": response.model
        }
        
        # End the run with outputs
        rt.end(outputs=result)
        rt.post()
        
        return result
        
    except Exception as e:
        # Log error and end run
        rt.error = str(e)
        rt.end()
        rt.post()
        raise

# Usage examples
premium_context = {
    "environment": "prod",
    "service": "analytics", 
    "user_tier": "premium",
    "user_id": "user-123",
    "session_id": "session-456",
    "feature_flags": ["advanced_analytics", "real_time_data"]
}

result = advanced_request_handler(
    premium_context,
    "Generate a quarterly revenue report with predictions"
)
# Logs to: "prod-analytics-premium" with rich metadata

basic_context = {
    "environment": "prod",
    "service": "support",
    "user_tier": "basic", 
    "user_id": "user-789"
}

result = advanced_request_handler(
    basic_context,
    "How do I change my password?"
)
# Logs to: "prod-support-basic"
```

### Multi-Tenant Application Example

Complete example for a multi-tenant SaaS application:

```python
import openai
from langsmith import traceable, wrappers
from typing import Dict, Any
import os

class MultiTenantAIService:
    def __init__(self):
        self.client = openai.Client()
        self.wrapped_client = wrappers.wrap_openai(self.client)
        self.environment = os.getenv("ENVIRONMENT", "dev")
    
    def get_project_name(self, tenant_id: str, service_type: str) -> str:
        """Generate consistent project names"""
        return f"{self.environment}-{service_type}-tenant-{tenant_id}"
    
    @traceable(
        run_type="llm",
        name="Chat Completion",
        project_name=lambda self, tenant_id, service_type, *args: 
            self.get_project_name(tenant_id, service_type)
    )
    def chat_completion(self, tenant_id: str, service_type: str, 
                       messages: list, **kwargs) -> Dict[str, Any]:
        """Tenant-specific chat completions"""
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            **kwargs
        )
        
        return {
            "content": response.choices[0].message.content,
            "tenant_id": tenant_id,
            "service_type": service_type,
            "project": self.get_project_name(tenant_id, service_type),
            "tokens": response.usage.total_tokens
        }
    
    def wrapped_chat_completion(self, tenant_id: str, service_type: str, 
                               messages: list, **kwargs) -> str:
        """Alternative using wrapped client"""
        project_name = self.get_project_name(tenant_id, service_type)
        
        response = self.wrapped_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            langsmith_extra={"project_name": project_name},
            **kwargs
        )
        
        return response.choices[0].message.content

# Usage
ai_service = MultiTenantAIService()

# Different tenants, different projects
tenant_a_result = ai_service.chat_completion(
    "company-a",
    "customer-support", 
    [{"role": "user", "content": "How do I cancel my subscription?"}]
)
# Logs to: "dev-customer-support-tenant-company-a"

tenant_b_result = ai_service.chat_completion(
    "company-b",
    "data-analysis",
    [{"role": "user", "content": "Analyze last month's sales data"}]
)
# Logs to: "dev-data-analysis-tenant-company-b"
```

### Best Practices

#### Dynamic Project Logging

1. **Consistent Naming Conventions**: Use predictable patterns for project names
2. **Environment Separation**: Include environment in project names  
3. **Error Handling**: Always handle exceptions in RunTree usage
4. **Metadata Management**: Include relevant context in tags and metadata
5. **Project Name Limits**: Keep project names under reasonable length limits
6. **Fallback Projects**: Have default projects for error scenarios

#### Organizational Structure

7. **Use Resource Tags for Environment Separation**: Never create separate workspaces for dev/staging/prod environments. Use resource tags with the "Environment" key instead.

8. **Reserve Workspaces for Trust Boundaries**: Only create new workspaces for different teams, security contexts, or regulatory isolation requirements.

9. **Plan Resource Sharing**: Keep resources that need to share datasets, prompts, or evaluation results within the same workspace.

10. **Implement Tag Governance**: Establish consistent tagging standards before scaling your LangSmith usage across teams.

#### Multi-Agent Systems

11. **Agent Hierarchy Tagging**: Use consistent tags to identify main orchestrators vs sub-agents (`"agent-type": "main"` vs `"agent-type": "sub-agent"`).

12. **Department-Specific Organization**: Tag resources by business department or service area (`"department": "housekeeping"`, `"department": "maintenance"`).

13. **Cross-Agent Tracing**: Use RunTree parent-child relationships to track request flows from orchestrator to sub-agents.

#### Resource Management

14. **Current Limitations Awareness**: Resource tags are currently UI-managed only. Plan for future programmatic API support.

15. **Future-Proof Tag Design**: Design your tag taxonomy assuming programmatic management will become available.

16. **Monitor API Evolution**: Stay updated on LangSmith SDK releases for enhanced resource tagging capabilities.

This approach enables you to maintain a single codebase while achieving precise trace organization across different contexts, environments, and use cases, while properly leveraging LangSmith's organizational hierarchy.

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

Use appropriate decorators for tracing<sup>[[2]](https://www.langchain.com/langsmith)</sup>:

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

Configure online evaluation rules for production<sup>[[9]](https://www.datacamp.com/tutorial/introduction-to-langsmith)</sup>:

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

## Troubleshooting

### Common Misconceptions and Issues

#### Workspace vs Resource Tags Confusion

**Problem**: "I created separate workspaces for dev, staging, and prod environments"
**Why it's problematic**:
- Cannot share datasets or prompts across workspaces
- Increases management complexity
- Creates unnecessary resource isolation
- Violates LangSmith's recommended architecture

**Solution**: 
- Use a single workspace for your application/team
- Separate environments using resource tags with `"environment": "dev|staging|prod"`
- Migrate resources to a unified workspace structure

#### Missing Resource Tags Features

**Problem**: "I can't find the resource tags in my LangSmith workspace"
**Common causes**:
- Using Free tier (resource tags require Plus or Enterprise)
- Using older version of LangSmith (feature released August 2024)
- Looking in wrong location in UI

**Solution**:
- Verify your plan tier supports resource tags
- Update to latest LangSmith version
- Access tags via: Resource Detail Page → "Resource tags" button
- Manage tag keys via: Workspace Settings → Resource Tags

#### Programmatic Resource Tagging Limitations

**Problem**: "My Python code can't set resource tags when creating datasets/projects"
**Why it doesn't work**:
- Resource tagging API is not yet fully available in SDK
- Only dataset version tagging is currently supported programmatically
- General resource tagging is primarily UI-managed as of 2024

**Current workaround**:
- Set up tag taxonomy through UI first
- Plan for future API support by designing consistent tag structure
- Use UI-based tag assignment for now
- Monitor SDK updates for enhanced programmatic support

#### Multi-Agent Tracing Visibility Issues

**Problem**: "I can't see the relationship between my main agent and sub-agents in traces"
**Common causes**:
- Missing parent-child trace relationships
- Sub-agents not logging to related projects  
- Inconsistent tagging across agent types
- Projects not properly organized by function

**Solution**:
```python
# Ensure parent-child trace relationship
@traceable(project_name="hotel-agent-prod-main")
def main_orchestrator(request):
    # Process main request
    result = sub_agent_call(request, parent_context=get_current_trace())
    return result

@traceable(project_name="hotel-agent-prod-housekeeping")  
def housekeeping_agent(request, parent_context):
    # Maintain trace hierarchy
    return process_housekeeping_request(request)
```

#### Tag Naming Inconsistencies

**Problem**: "Our tags are inconsistent and hard to filter by"
**Common issues**:
- Mixed case (`Dev` vs `dev` vs `DEV`)
- Inconsistent separators (`front_desk` vs `front-desk` vs `frontdesk`)
- Verbose values (`production-environment` vs `prod`)

**Solution**:
- Establish tag naming conventions document
- Use lowercase with hyphens: `front-desk`, `hotel-agent`
- Standardize environment values: `dev`, `staging`, `prod`
- Create controlled vocabularies for tag values

#### Resource Discovery and Organization

**Problem**: "I have too many projects and can't find what I need"
**Organizational strategies**:

**By Environment**:
```
Projects filtered by environment tag:
├── dev: All development projects
├── staging: Pre-production testing  
└── prod: Production systems
```

**By Application**:
```
Projects filtered by application tag:
├── hotel-agent: All hotel AI agent projects
├── analytics: Business intelligence projects
└── customer-portal: Customer-facing applications  
```

**By Team/Ownership**:
```
Projects filtered by owner tag:
├── ai-platform-team: ML/AI projects
├── data-team: Data processing projects
└── operations-team: Infrastructure projects
```

### Debugging Resource Tag Issues

#### Verify Tag Configuration

1. **Check Workspace Settings**:
   - Navigate to Workspace Settings → Resource Tags
   - Verify tag keys exist and have proper values
   - Ensure tag permissions are correctly set

2. **Validate Resource Tag Assignment**:
   - Go to resource detail page (Project, Dataset, etc.)
   - Click "Resource tags" button
   - Verify tags are assigned with correct values

3. **Test Tag Filtering**:
   - Use workspace resource list views
   - Apply tag filters to verify they work
   - Check that expected resources appear

#### Plan Migration Strategy

If you need to restructure your LangSmith organization:

1. **Audit Current Structure**:
   - Document existing workspaces and their purposes  
   - Identify resources that should be consolidated
   - Map current naming conventions

2. **Design Target Structure**:
   - Plan workspace consolidation strategy
   - Define resource tag taxonomy
   - Create migration timeline

3. **Execute Migration**:
   - Start with non-production resources
   - Test tag filtering and resource discovery
   - Update team documentation and processes

4. **Monitor and Iterate**:
   - Gather team feedback on new structure
   - Refine tag taxonomy based on usage patterns
   - Document lessons learned for future scaling

### Getting Help

#### LangSmith Support Channels

- **Documentation**: https://docs.smith.langchain.com
- **GitHub Issues**: https://github.com/langchain-ai/langsmith-sdk/issues  
- **Discord Community**: LangChain Discord server
- **Enterprise Support**: Contact your LangSmith account team

#### When to Contact Support

- Resource tags not appearing despite Plus/Enterprise plan
- Unexpected behavior with workspace permissions
- SDK functionality not matching documented API
- Performance issues with large-scale resource organization

## References

[1]: [LangSmith Concepts - Resource Organization](https://docs.smith.langchain.com/administration/concepts) - Official documentation on workspace organization and resource tagging

[2]: [LangSmith Web Search Results](https://www.langchain.com/langsmith) - General LangSmith platform information and best practices

[3]: [LangSmith Walkthrough](https://python.langchain.com/v0.1/docs/langsmith/walkthrough/) - Python SDK walkthrough with environment setup

[4]: [Get started with LangSmith](https://docs.smith.langchain.com/) - Official getting started guide with configuration examples

[5]: [Log traces to specific project](https://docs.smith.langchain.com/observability/how_to_guides/log_traces_to_project) - Documentation on project-specific logging

[6]: [Evaluation concepts](https://docs.smith.langchain.com/evaluation/concepts) - Comprehensive guide to offline and online evaluation

[7]: [Creating and Managing Datasets in the UI](https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_in_application) - Dataset management documentation

[8]: [Evaluation how-to guides](https://docs.smith.langchain.com/evaluation/how_to_guides) - Collection of evaluation best practices

[9]: [An Introduction to Debugging And Testing LLMs in LangSmith](https://www.datacamp.com/tutorial/introduction-to-langsmith) - Third-party tutorial with practical examples

[10]: [LangSmith Administration Concepts](https://docs.smith.langchain.com/administration/concepts) - Comprehensive guide to organizational hierarchy, workspaces, and resource management

### Additional Resources

- [GitHub: langchain-ai/helm](https://github.com/langchain-ai/helm) - Official Helm charts for Kubernetes deployment
- [GitHub: langchain-ai/intro-to-langsmith](https://github.com/langchain-ai/intro-to-langsmith) - Tutorial repository with examples
- [Self-hosting LangSmith](https://docs.smith.langchain.com/self_hosting) - Documentation for enterprise self-hosting options
- [LangSmith API Reference](https://api.smith.langchain.com/redoc) - Complete API documentation
