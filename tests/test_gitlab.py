import pytest

from ai_code_reviewer.gitlab import get_diffs, post_comment


@pytest.mark.parametrize('pid, mr_id', [
  (10, 1)
])
def test_get_diffs(pid, mr_id):
  res = get_diffs(pid, mr_id)
  assert res
  diffs = [change["diff"] for change in res["changes"]]
  assert diffs
