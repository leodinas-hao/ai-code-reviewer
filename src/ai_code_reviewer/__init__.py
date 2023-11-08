import os

from dotenv import load_dotenv

from .utils import init_logger

# load the env
load_dotenv(os.path.join(os.getcwd(), '.env'))

# setup logging
init_logger(2)
