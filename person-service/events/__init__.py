from typing import NamedTuple, Callable


class Config(NamedTuple):
    """
    Defines the configuration properties for creating events.
    """

    schema: str
    """
    Name of the schema to use.
    """

    topic: str
    """
    The topic name (subject) the schema will be registred to.
    """

    to_dict: Callable[[object, object], dict]
    """
    function that takes a model and a context object and returns a dictionary
    matching the target schema.
    """
