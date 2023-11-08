import os

import pytest
from dotenv import load_dotenv

from ai_code_reviewer.utils import init_logger


@pytest.fixture(scope='session', autouse=True)
def setup():
  # load the env
  load_dotenv(os.path.join(os.getcwd(), '.env'))

  # set logging level to DEBUG
  init_logger(2)
