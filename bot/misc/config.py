from abc import ABC
from typing import Final


class BotConfig(ABC):
    CMD_PREFIX: Final = '/'
