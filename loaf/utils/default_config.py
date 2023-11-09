from enum import Enum

from .cursor_types import CursorTypes
from .database_types import DatabaseTypes


class DefaultConfig(Enum):
    HOST = "localhost"
    PORT = 3306
    USER = "root"
    PASSWORD = ""
    DATABASE = None
    CURSOR_TYPE = CursorTypes.DICTIONARY
    DATABASE_TYPE = DatabaseTypes.MYSQL
    ROLLBACK_ON_ERROR = True
    