import logging
from typing import List

from openai.types.chat import ChatCompletionMessageParam

from .utils import chat_openai


CODE_REVIEW_PROMPT = '''As a senior developer, review the following code changes and answer code review questions about them. The code changes are provided as git diff strings:'''

CODE_REVIEW_QUESTIONS = '''
Questions:
1. Can you summarise the changes in a succinct bullet point list
2. In the diff, are the added or changed code written in a clear and easy to understand way?
3. Does the code use comments, or descriptive function and variables names that explain what they mean?
4. based on the code complexity of the changes, could the code be simplified without breaking its functionality? if so can you give example snippets?
5. Can you find any bugs, if so please explain and reference line numbers?
6. Do you see any codes that could induce security issues?
'''


def messages(diffs: List[str]) -> List[ChatCompletionMessageParam]:
  '''generates open ai code review questions based on the provided code diffs'''

  return [
    {
      "role": "system",
      "content": "You are a senior developer reviewing code changes."
    },
    {
      "role": "user",
      "content": f"{CODE_REVIEW_PROMPT}\n\n{''.join(diffs)}{CODE_REVIEW_QUESTIONS}"
    },
    {
      "role": "assistant",
      "content": "Format the response so it renders nicely in GitLab, with nice and organized markdown (use code blocks if needed), and send just the response no comments on the request, when answering include a short version of the question, so we know what it is."
    },
  ]


def review(diffs: List[str]) -> str:
  '''get the responses from openai of the code review questions'''

  answer = ''
  logger = logging.getLogger(__name__)
  try:
    res = chat_openai(messages(diffs), temperature=0.7, stream=False)
    answer = f'{res.choices[0].message.content}'.strip()

    # log the response
    logger.debug(f'Received OpenAI response: {answer}')

    # format
    answer += "\n\nThe above response was produced to address the following questions: \n"
    for question in CODE_REVIEW_QUESTIONS.split("\n"):
      answer += f"\n{question}"
    answer += "\n\n**This comment was produced by AI code reviewer.**"
  except Exception as err:
    logger.warning(f'OpenAI Error: {err}', extra={'error': err})
    answer = "I'm sorry, I'm not feeling well today. Please ask a human to review this PR."
    answer += "\n\n**This comment was produced by AI code reviewer.**"
    answer += "\n\nError: " + str(err)
  finally:
    return answer
