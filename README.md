# aws-todo-api

A tiny **serverless TODO API** on AWS with **PR-gated CI** and automated **CD**.

- **API**: API Gateway (HTTP API) → Lambda (`todo-api-dev`) → DynamoDB (`todo-dev`)
- **CI (PR checks)**: AWS CodeBuild (`todo-ci`) runs linting (ruff), formatting check (black), and tests (pytest + moto)
- **CD (on main)**: CodePipeline → CodeBuild (`todo-cd`) packages and updates the Lambda
- **Observability**: CloudWatch Logs & Metrics (+ optional alarm → SNS)

---

## Architecture 

**Developer workflow:**
1. Dev pushes to a **feature branch** in GitHub
2. Open a **Pull Request** → CodeBuild (`todo-ci`) runs tests + lint
3. If checks pass, merge to `main`
4. CodePipeline runs → CodeBuild (`todo-cd`) updates the Lambda

**Runtime:**
- Client → **API Gateway** → **Lambda** (`todo-api-dev`) ↔ **DynamoDB** (`todo-dev`)
- Logs + metrics in **CloudWatch**




