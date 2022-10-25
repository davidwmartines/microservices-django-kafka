from typing import NamedTuple, Callable


class Config(NamedTuple):
    schema: str
    topic: str
    to_dict: Callable[[object, object], dict]
