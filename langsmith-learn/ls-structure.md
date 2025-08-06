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
12. [Troubleshooting](#troubleshooting)
13. [References](#references)

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

### LangSmith 3-Tier Structure

LangSmith uses a simple hierarchy for access control and resource management:

```
Organization (Company)
└── Workspace (Team/Trust Boundary)
    ├── Projects (Where traces are logged)
    ├── Datasets (Evaluation data)  
    ├── Prompts (Template management)
    └── Other Resources
```

### When to Create Workspaces

**✅ Create separate workspaces for**:
- Different teams (e.g., "AI-Platform", "Data-Team")
- Different security contexts (e.g., "Internal", "Customer-Facing") 
- Regulatory isolation (e.g., "HIPAA-Compliant")

**❌ Don't create workspaces for**:
- Environment separation (dev/staging/prod) - Use resource tags
- Temporary experiments - Use projects with clear naming

### Hotel Agent System Structure

For your hotel agent system, use one workspace with environment separation via tags:

```
organization: "hotel-management"
└── workspace: "ai-platform-team"
    ├── projects: hotel-agent-dev-orchestrator, hotel-agent-dev-housekeeping, etc.
    ├── projects: hotel-agent-prod-orchestrator, hotel-agent-prod-housekeeping, etc.
    ├── datasets: [housekeeping-scenarios, maintenance-requests, front-desk-procedures]
    └── prompts: [orchestrator-prompts, department-prompts]
```

**Key Point**: Resources cannot be shared across workspaces, so keep related resources (datasets, prompts, projects) in the same workspace and use tags for organization.

## Environment Configuration

### Required Environment Variables

LangSmith requires the following environment variables<sup>[[3]](https://python.langchain.com/v0.1/docs/langsmith/walkthrough/)</sup><sup>[[4]](https://docs.smith.langchain.com/)</sup>:

```bash
# Required
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=<YOUR-LANGSMITH-API-KEY>
LANGCHAIN_PROJECT=<YOUR-PROJECT-NAME>
```

### Environment-Specific Files

**.env.development**
```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls__dev_xxxxxx
LANGSMITH_PROJECT=hotel-agent-dev-main
LANGSMITH_VERBOSE=true
```

**.env.production**
```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls__prod_xxxxxx
LANGSMITH_PROJECT=hotel-agent-prod-main
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

### Essential Tag Structure for Hotel Agent System

Use these core tags to organize your hotel agent resources:

```python
# Basic tag structure for hotel agents
hotel_agent_tags = {
    # Environment separation (required)
    "environment": "dev|staging|prod",
    "application": "hotel-agent",
    
    # Agent organization
    "component": "orchestrator|housekeeping-agent|maintenance-agent|front-desk-agent",
    "agent-type": "main|sub-agent",
    "department": "housekeeping|maintenance|front-desk|concierge",
    
    # Operational
    "team": "ai-platform-team",
    "lifecycle": "active|experimental|deprecated"
}
```

### Multi-Agent Tagging Pattern

Organize your hotel system components:

```python
# Main orchestrator
orchestrator_tags = {
    "environment": "prod",
    "application": "hotel-agent",
    "component": "orchestrator",
    "agent-type": "main",
    "department": "all"
}

# Department-specific agents
housekeeping_tags = {
    "environment": "prod", 
    "application": "hotel-agent",
    "component": "housekeeping-agent",
    "agent-type": "sub-agent",
    "department": "housekeeping"
}

maintenance_tags = {
    "environment": "prod",
    "application": "hotel-agent", 
    "component": "maintenance-agent",
    "agent-type": "sub-agent",
    "department": "maintenance"
}
```

### Current Limitations

**UI-Based Management Only** (as of 2024):
- Resource tags must be set through LangSmith UI
- No SDK support for general resource tagging
- Plan your tag structure now for future API support

**Setting Tags**:
1. Navigate to resource detail page (Project, Dataset, etc.)
2. Click "Resource tags" button
3. Assign key-value pairs
4. Save changes

## Evaluation Workflows

### Basic Pipeline

LangSmith supports both offline and online evaluation workflows<sup>[[6]](https://docs.smith.langchain.com/evaluation/concepts)</sup>:

1. **Development**: Test on small datasets (10-50 examples), rapid iteration
2. **Staging**: Regression testing with larger datasets (100-1000 examples)  
3. **Production**: Online monitoring with sampling and automated alerts

Use LangSmith's offline evaluation for pre-deployment testing and online evaluation for production monitoring.

## Dataset Management

### Dataset Creation

LangSmith offers multiple methods for dataset creation<sup>[[7]](https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_in_application)</sup>:
- **From traces**: Convert production traces to datasets
- **Manual**: Through UI or SDK
- **Import**: CSV/JSONL files

### Naming Convention
```
{environment}-{purpose}-{version}
Examples: dev-housekeeping-scenarios-v1, prod-user-feedback-v2
```

### Dataset Splits

Divide datasets into training, validation, and test sets to prevent overfitting<sup>[[8]](https://docs.smith.langchain.com/evaluation/how_to_guides)</sup>.

## Dynamic Project Logging

### Overview

Dynamic project logging allows you to log traces to different LangSmith projects at runtime, organizing traces by environment, agent type, or hotel department while using the same codebase<sup>[[5]](https://docs.smith.langchain.com/observability/how_to_guides/log_traces_to_project)</sup>.

### Prerequisites

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=your_api_key_here
```

### Method 1: Static Project Assignment

Use `project_name` in the `@traceable` decorator for fixed project assignments:

```python
import openai
from langsmith import traceable

client = openai.Client()

@traceable(
    run_type="llm",
    name="Hotel Orchestrator",
    project_name="hotel-agent-prod-main"
)
def main_orchestrator(request: str) -> dict:
    """All main orchestrator traces go to hotel-agent-prod-main"""
    messages = [
        {"role": "system", "content": "You are the main hotel agent orchestrator."},
        {"role": "user", "content": request}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    return {
        "response": response.choices[0].message.content,
        "agent_type": "orchestrator"
    }

@traceable(
    run_type="llm", 
    name="Housekeeping Agent",
    project_name="hotel-agent-prod-housekeeping"
)
def housekeeping_agent(task: str) -> dict:
    """All housekeeping traces go to hotel-agent-prod-housekeeping"""
    messages = [
        {"role": "system", "content": "You are the housekeeping department agent."},
        {"role": "user", "content": task}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    return {
        "response": response.choices[0].message.content,
        "department": "housekeeping"
    }
```

### Method 2: Runtime Project Override

Override project assignment at runtime using `langsmith_extra`:

```python
@traceable(
    run_type="llm",
    name="Hotel Agent Handler",
    project_name="default-project"  # Gets overridden
)
def handle_hotel_request(department: str, environment: str, request: str) -> str:
    """Route requests to department and environment-specific projects"""
    messages = [
        {"role": "system", "content": f"You are the {department} agent."},
        {"role": "user", "content": request}
    ]
    
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    ).choices[0].message.content

# Usage examples - same function, different projects
# Development housekeeping
dev_result = handle_hotel_request(
    "housekeeping", 
    "dev", 
    "Schedule room cleaning for room 204",
    langsmith_extra={"project_name": "hotel-agent-dev-housekeeping"}
)

# Production maintenance
prod_result = handle_hotel_request(
    "maintenance",
    "prod", 
    "Fix broken AC in room 301",
    langsmith_extra={"project_name": "hotel-agent-prod-maintenance"}
)
```

### Hotel Agent System Example

Complete example for your multi-agent hotel system:

```python
import openai
from langsmith import traceable
import os

class HotelAgentService:
    def __init__(self):
        self.client = openai.Client()
        self.environment = os.getenv("ENVIRONMENT", "dev")
    
    def get_project_name(self, department: str) -> str:
        """Generate consistent project names for hotel departments"""
        return f"hotel-agent-{self.environment}-{department}"
    
    @traceable(
        run_type="llm",
        name="Department Handler",
        project_name=lambda self, department, *args: 
            self.get_project_name(department)
    )
    def handle_department_request(self, department: str, request: str) -> dict:
        """Route to department-specific projects"""
        
        system_messages = {
            "orchestrator": "You are the main hotel orchestrator managing all departments.",
            "housekeeping": "You are the housekeeping agent managing room cleaning and maintenance.",
            "maintenance": "You are the maintenance agent handling repairs and technical issues.",
            "front-desk": "You are the front desk agent managing guest check-in/out and reservations."
        }
        
        messages = [
            {"role": "system", "content": system_messages.get(department, "You are a hotel service agent.")},
            {"role": "user", "content": request}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        return {
            "response": response.choices[0].message.content,
            "department": department,
            "project": self.get_project_name(department)
        }

# Usage
hotel_service = HotelAgentService()

# Routes to: "hotel-agent-dev-orchestrator"
orchestrator_result = hotel_service.handle_department_request(
    "orchestrator",
    "Guest in room 205 needs assistance with multiple issues"
)

# Routes to: "hotel-agent-dev-housekeeping"  
housekeeping_result = hotel_service.handle_department_request(
    "housekeeping",
    "Room 301 needs deep cleaning after checkout"
)

# Routes to: "hotel-agent-dev-maintenance"
maintenance_result = hotel_service.handle_department_request(
    "maintenance", 
    "Air conditioning not working in room 205"
)
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

```python
# langsmith_config.py
import os

def get_langsmith_config(environment: str) -> dict:
    """Load environment-specific LangSmith configuration"""
    return {
        "tracing": os.getenv("LANGSMITH_TRACING", "true"),
        "api_key": os.getenv("LANGSMITH_API_KEY"),
        "project": os.getenv("LANGSMITH_PROJECT"),
        "environment": environment,
        "application": "hotel-agent"
    }
```

### Basic Usage

Use `@traceable` decorator for tracing and include relevant metadata:

```python
from langsmith import traceable

@traceable(project_name="hotel-agent-prod-main")
def hotel_function():
    # Your code here
    pass
```



## Troubleshooting

### Common Setup Issues

#### Workspace vs Tags Confusion

**Problem**: Created separate workspaces for dev/staging/prod environments
**Why it's wrong**: Cannot share datasets or prompts across workspaces
**Solution**: Use one workspace with resource tags for environment separation

#### Missing Resource Tags

**Problem**: Can't find resource tags in LangSmith workspace
**Common causes**: 
- Free tier (requires Plus/Enterprise)
- Feature released August 2024
**Solution**: Upgrade plan, access via Resource Detail Page → "Resource tags" button

#### Can't Set Tags Programmatically

**Problem**: Python code can't set resource tags
**Why**: Resource tagging API not fully available in SDK yet (2024)
**Workaround**: Set up tag structure in UI, plan for future API support

#### Multi-Agent Trace Visibility

**Problem**: Can't see relationships between main and sub-agents
**Solution**: Use consistent project naming and ensure trace parent-child relationships:

```python
@traceable(project_name="hotel-agent-prod-main")
def main_orchestrator(request):
    result = sub_agent_call(request, parent_context=get_current_trace())
    return result

@traceable(project_name="hotel-agent-prod-housekeeping")  
def housekeeping_agent(request, parent_context):
    return process_housekeeping_request(request)
```

#### Inconsistent Tag Naming

**Problem**: Mixed naming (`Dev` vs `dev`, `front_desk` vs `front-desk`)
**Solution**: 
- Use lowercase with hyphens: `hotel-agent`, `front-desk`
- Standardize values: `dev`, `staging`, `prod`
- Document naming conventions

### Getting Help

- **Documentation**: https://docs.smith.langchain.com
- **GitHub Issues**: https://github.com/langchain-ai/langsmith-sdk/issues  
- **Discord**: LangChain Discord server

## References

[1]: [LangSmith Concepts - Resource Organization](https://docs.smith.langchain.com/administration/concepts) - Official documentation on workspace organization and resource tagging

[2]: [LangSmith Web Search Results](https://www.langchain.com/langsmith) - General LangSmith platform information and best practices

[3]: [LangSmith Walkthrough](https://python.langchain.com/v0.1/docs/langsmith/walkthrough/) - Python SDK walkthrough with environment setup

[4]: [Get started with LangSmith](https://docs.smith.langchain.com/) - Official getting started guide with configuration examples

[5]: [Log traces to specific project](https://docs.smith.langchain.com/observability/how_to_guides/log_traces_to_project) - Documentation on project-specific logging

[6]: [Evaluation concepts](https://docs.smith.langchain.com/evaluation/concepts) - Comprehensive guide to offline and online evaluation

[7]: [Creating and Managing Datasets in the UI](https://docs.smith.langchain.com/evaluation/how_to_guides/manage_datasets_in_application) - Dataset management documentation

[8]: [Evaluation how-to guides](https://docs.smith.langchain.com/evaluation/how_to_guides) - Collection of evaluation best practices

[10]: [LangSmith Administration Concepts](https://docs.smith.langchain.com/administration/concepts) - Comprehensive guide to organizational hierarchy, workspaces, and resource management
