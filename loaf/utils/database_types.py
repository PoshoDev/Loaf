from enum import Enum, auto


class DatabaseTypes(Enum):
    MYSQL = auto()
    POSTGRESQL = auto()
    SQLITE = auto()