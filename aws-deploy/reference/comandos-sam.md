# Useful SAM CLI Commands

```bash
# View logs from deployed function
sam logs -n MyFunction --tail

# Local invoke for testing
sam local invoke MyFunction -e event.json

# Start local API Gateway
sam local start-api

# Validate template
sam validate

# Delete stack
sam delete --stack-name my-app-dev
```
