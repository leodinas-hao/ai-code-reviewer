from logging import config
import os
from typing import List

from openai import AzureOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

DEFAULT_LOGGER_CONFIG = {
  'version': 1,
  'root': {
    'level': 'DEBUG',
    'handlers': ['console', 'file']
  },
  'handlers': {
    'console': {
      'formatter': 'stdout',
      'class': 'logging.StreamHandler',
      'level': 'WARNING',
      # use stdout instead of default stderr
      # 'stream': 'ext://sys.stdout',
    },
    'file': {
      'formatter': 'json',
      'class': 'logging.FileHandler',
      'level': 'DEBUG',
      'filename': 'logs.log',
      # file opening is deferred until the first call
      'delay': True,
    },
  },
  'formatters': {
    'stdout': {
      'format': '%(asctime)s : %(levelname)s - %(name)s : %(message)s',
      'datefmt': '%Y-%m-%dT%H:%M:%S%z',
    },
    'json': {
      'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
      'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
      'datefmt': '%Y-%m-%dT%H:%M:%S%z',
    }
  },
  'loggers': {
    # overwrite the logging level for urllib3 library, which is a dependency of requests
    # to avoid propagated logs from it
    'urllib3': {
      'level': 'WARNING',
      'propagate': False,
    },
    'httpcore': {
      'level': 'WARNING',
      'propagate': False,
    },
    'httpx': {
      'level': 'WARNING',
      'propagate': False,
    },
  },
  # https://docs.python.org/3/howto/logging.html#configuring-logging
  'disable_existing_loggers': False,
}


VERBOSE_MAP = [
  'WARNING',  # 0
  'INFO',     # 1
  'DEBUG',    # 2
]


def init_logger(verbose: int = 0, log_file: str = 'logs.log'):
  '''configures logger

  :param verbose (int, optional): verbosity level of console logger; default to 0; see `VERBOSE_MAP`
  :param log_file (str, optional): path of logger config; default to 'logs.log'
  '''

  # update console logging level
  DEFAULT_LOGGER_CONFIG['handlers']['console']['level'] = VERBOSE_MAP[verbose if verbose < 3 else 2]

  # update log file path
  DEFAULT_LOGGER_CONFIG['handlers']['file']['filename'] = log_file

  # set logger
  config.dictConfig(DEFAULT_LOGGER_CONFIG)


def openai_client():
  '''shortcut to get openai client'''

  if os.getenv('AZURE_OPENAI_ENDPOINT') is None:
    raise ValueError('AZURE_OPENAI_ENDPOINT cannot be omitted')

  if os.getenv('AZURE_OPENAI_KEY') is None:
    raise ValueError('AZURE_OPENAI_KEY cannot be omitted')

  if os.getenv('AZURE_OPENAI_VERSION') is None:
    raise ValueError('AZURE_OPENAI_VERSION cannot be omitted')

  return AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_KEY'),
    api_version=os.getenv('AZURE_OPENAI_VERSION'),
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
  )


def chat_openai(messages: List[ChatCompletionMessageParam], *, temperature=0.7, **kwargs) -> ChatCompletion:
  '''shortcut to chat open ai'''

  params = {
    'model': os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
    'messages': messages,
    'temperature': temperature,
    **kwargs,
  }

  return openai_client().chat.completions.create(**params)
