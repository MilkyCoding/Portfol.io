import os
from abc import ABC
from typing import Final
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Env(ABC):
    TOKEN: Final = os.environ.get('TOKEN', 'define me!')
