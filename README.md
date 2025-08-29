# aws-todo-api

A tiny **serverless TODO API** on AWS with **PR-gated CI** and automated **CD**.

- **API**: API Gateway (HTTP API) → Lambda (`todo-api-dev`) → DynamoDB (`todo-dev`)
- **CI (PR checks)**: AWS CodeBuild (`todo-ci`) runs linting (ruff), formatting check (black), and tests (pytest + moto)
- **CD (on main)**: CodePipeline → CodeBuild (`todo-cd`) packages and updates the Lambda
- **Observability**: CloudWatch Logs & Metrics (+ optional alarm → SNS)



