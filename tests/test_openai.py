import os
import logging

import pytest

from ai_code_reviewer.utils import chat_openai, openai_client


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
