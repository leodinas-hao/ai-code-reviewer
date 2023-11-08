import os
import logging

from flask import Flask, request

from .code_review import review
from .gitlab import get_diffs, post_comment

# get gitlab webhook info
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 8080))
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')


# add logger
logger = logging.getLogger(__name__)

# setup flask app
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
  if request.headers.get("X-Gitlab-Token") != WEBHOOK_TOKEN:
    return "Unauthorized", 403

  logger.info(f'Received event: {request.data}')

  payload = request.json
  if payload and payload.get("object_kind") == "merge_request":
    # a merge request received
    if payload["object_attributes"]["state"] == "opened":
      # only review open request
      project_id = payload["project"]["id"]
      merge_request_id = payload["object_attributes"]["iid"]
      logger.info(f'Reviewing the merge request', extra={'project': project_id, 'merge_request': merge_request_id})

      # get changes
      merge_request_changes = get_diffs(project_id, merge_request_id)
      diffs = [change["diff"] for change in merge_request_changes["changes"]]

      # ask chatgpt to review
      logger.info(f'Asking chatgpt to review the changes', extra={'diffs': diffs})
      answer = review(diffs)

      # send comment to gitlab
      logger.info(f'Posting code review comments back to the merge request', extra={'project': project_id, 'merge_request': merge_request_id})
      comment_response = post_comment(project_id, merge_request_id, answer)
      logger.info(f'Code review comment added to the merge request', extra={
        'response': comment_response, 'project': project_id, 'merge_request': merge_request_id,
      })

  return "OK", 200


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=WEBHOOK_PORT)
