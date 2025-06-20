from enum import Enum

class AuditorLevel(Enum):
    """
    Represents the level of an auditor in the system.
    """

    DEFAULT = "default"
    STRICT = "strict"

    def __init__(self, level: int):
        self.level = level

    def __str__(self):
        return f"AuditorLevel(level={self.level})"

    def __repr__(self):
        return self.__str__()