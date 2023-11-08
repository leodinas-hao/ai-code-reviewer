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

## to setup
```powershell
# clone the project
git clone https://gitlab.macquarietelecom.com/lhao/ai-code-reviewer.git

cd ai-code-reviewer

# put environment variables
touch .env

# setup venv
python -m venv .venv
# activate venv on windows
.\.venv\Scripts\activate
# check if venv works
where.exe pip
# install dependencies
pip install -r requirements.txt
# to deactivate
deactivate

# alternatively, setup via pipenv
python -m pip install pipenv  # only if pipenv not installed yet
# init venv
pipenv shell
# install dependencies
pipenv install
```

## to run the web listener
```sh
# to run the app
.\.venv\Scripts\python.exe -m src.ai_code_reviewer.app
```

## .env
```
# example format of .env
OPENAI_API_KEY=<OPENAI_API_KEY>
OPENAI_API_BASE=<AZURE_API_BASE_URL>
OPENAI_API_VERSION=<AZURE_OPENAI_VERSION>

GITLAB_TOKEN=<GITLAB_ACCESS_TOKEN>
GITLAB_URL=<GITLAB_URL>/api/v4

WEBHOOK_TOKEN=<GITLAB_WEBHOOK_TOKEN>
WEBHOOK_PORT=<WEBHOOK_PORT>
```
