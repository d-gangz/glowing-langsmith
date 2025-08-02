# LangSmith Learnings

This document consolidates key learnings and insights from working with LangSmith.

## Environment Configuration

### API Endpoint Configuration

- **Learning**: Must set `LANGCHAIN_ENDPOINT` in `.env` file to direct to the correct regional URL
- **Issue**: Without this, API calls may fail with 403 Forbidden errors
- **Solution**: Add to `.env`:
  ```
  LANGCHAIN_ENDPOINT=https://eu.api.smith.langchain.com  # For EU region
  ```
  or
  ```
  LANGCHAIN_ENDPOINT=https://api.smith.langchain.com     # For US region (default)
  ```

### Environment Variables

Key environment variables for LangSmith:

- `LANGSMITH_API_KEY`: Your API key
- `LANGCHAIN_ENDPOINT`: Regional API endpoint
- `LANGCHAIN_TRACING_V2`: Set to "true" to enable tracing

## API Key Types

- **Personal Access Token**: For individual user authentication (local development)
- **Service Key**: For automated systems and CI/CD workflows

## Common Issues and Solutions

### 403 Forbidden Errors

- Check if using the correct regional endpoint
- Verify API key has proper permissions
- Ensure account/workspace has required features enabled

### Dataset Creation

- Some features may require paid plans
- Free tier accounts may have limitations on dataset operations

## Best Practices

1. Always use environment variables for API keys
2. Set the correct regional endpoint based on your account location
3. Enable tracing with `LANGCHAIN_TRACING_V2=true` for better debugging
4. Test API connectivity before attempting complex operations
