import os

import requests


# get gitlab api credentials
GITLAB_URL = os.getenv('GITLAB_URL', '').rstrip('/')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN', '')

GITLAB_API = f'{GITLAB_URL}/api/v4'


def get_diffs(project_id, merge_request_id):
  '''gets merge request diffs'''

  url = f'{GITLAB_API}/projects/{project_id}/merge_requests/{merge_request_id}/changes'
  headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

  return requests.get(url, headers=headers).json()


def post_comment(project_id, merge_request_id, comment):
  '''posts a comment to the specified merge request'''

  url = f'{GITLAB_API}/projects/{project_id}/merge_requests/{merge_request_id}/notes'
  headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

  return requests.post(url, headers=headers, json={"body": comment}).json()
