import os
import logging

import pytest

from ai_code_reviewer.utils import chat_openai, openai_client
from ai_code_reviewer.gitlab import get_diffs, post_comment
from ai_code_reviewer.code_review import review


@pytest.mark.parametrize('prompt', [
  'Write a tagline for an ice cream shop'
])
def test_openai_client(prompt):
  client = openai_client()

  res = client.chat.completions.create(
    model=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Write a tagline for an ice cream shop."}
    ]
  )

  assert res.choices[0].message.content
  logging.getLogger(__name__).info(f'OpenAI response: {res.choices[0].message.content}')


@pytest.mark.parametrize('msgs', [
  [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a tagline for an ice cream shop."}
  ],
])
def test_chat_openai(msgs):
  res = chat_openai(msgs)
  assert res.choices[0].message.content
  logging.getLogger(__name__).info(f'OpenAI response: {res.choices[0].message.content}')


@pytest.mark.parametrize('pid, mr_id', [
  (10, 1)
])
def test_git_diff_code_review(pid, mr_id):
  res = get_diffs(pid, mr_id)
  diffs = [change["diff"] for change in res["changes"]]
  res = review(diffs)
  assert res

  res = post_comment(pid, mr_id, res)
  assert res
