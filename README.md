# aws-todo-api

A tiny **serverless TODO API** on AWS with **PR-gated CI** and automated **CD**.

- **API**: API Gateway (HTTP API) → Lambda (`todo-api-dev`) → DynamoDB (`todo-dev`)
- **CI (PR checks)**: AWS CodeBuild (`todo-ci`) runs linting (ruff), formatting check (black), and tests (pytest + moto)
- **CD (on main)**: CodePipeline → CodeBuild (`todo-cd`) packages and updates the Lambda
- **Observability**: CloudWatch Logs & Metrics (+ optional alarm → SNS)

---

## Architecture

```mermaid
flowchart LR
  subgraph Dev["Developer Workflow"]
    A[Feature branch<br/>GitHub] --> B[Pull Request]
    B -->|Webhook| C[CodeBuild CI<br/>(todo-ci)]
    C -->|Status| B
    B -->|Merge to main| D[CodePipeline]
    D --> E[CodeBuild CD<br/>(todo-cd)]
    E --> F[Lambda code update]
  end

  subgraph Runtime["Runtime"]
    G[Client / curl / browser] --> H[API Gateway /todo]
    H --> I[Lambda: todo-api-dev]
    I <--> J[(DynamoDB: todo-dev)]
    I --> K[CloudWatch Logs & Metrics]
  end


