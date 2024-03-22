# ai-merge-request-reviewer

## flow

```mermaid
sequenceDiagram
  participant user
  participant gitlab
  participant ai-code-reviewer
  participant Azure OpenAI

  user ->> gitlab: Submit Merge Request
  gitlab ->> ai-code-reviewer: Push the Merge Request event
  ai-code-reviewer ->> gitlab: Request commit details
  gitlab ->> ai-code-reviewer: Response commit details
  ai-code-reviewer ->> Azure OpenAI: Sends code review questions
  Azure OpenAI ->> ai-code-reviewer: Response code review feedback
  ai-code-reviewer ->> gitlab: Add code review feedback as Merge Request comment
  user -->> gitlab: Review Merge Request with feedback from AI
```


## .env
```
# example format of .env
PYTHONPATH=src

PIPENV_VENV_IN_PROJECT=1

# gitlab conf
GITLAB_URL=<gitlab_url>
GITLAB_TOKEN=<gitlab_token>

WEBHOOK_TOKEN=<gitlab_webhook_token>
WEBHOOK_PORT=<gitlab_webhook_port>


# Azure OpenAI credentials
AZURE_OPENAI_ENDPOINT=https://openaimtg.openai.azure.com/
AZURE_OPENAI_KEY=<openai_api_key>
```
