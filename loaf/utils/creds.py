from .cursor_types import CursorTypes
from .database_types import DatabaseTypes
from .default_config import DefaultConfig

class Creds:
    def __init__(
        self,
        host: str = DefaultConfig.HOST,
        port: int = DefaultConfig.PORT,
        user: str = DefaultConfig.USER,
        password: str = DefaultConfig.PASSWORD,
        database: str = DefaultConfig.DATABASE,
        cursor_type: CursorTypes = DefaultConfig.CURSOR_TYPE,
        database_type: DatabaseTypes = DefaultConfig.DATABASE_TYPE,
        rollback_on_error: bool = DefaultConfig.ROLLBACK_ON_ERROR
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.cursor_type = cursor_type
        self.database_type = database_type
        self.rollback_on_error = rollback_on_error