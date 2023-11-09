from .cursor_types import CursorTypes
from .database_types import DatabaseTypes
from .default_config import DefaultConfig
from .parse_sql_url import parse_sql_url
from .load_files import load_file

class Creds:
    def __init__(
        self,
        url: str = None,
        file_path = None,
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

        if url:
            parse_sql_url(self, url)
        if file_path:
            load_file(self, file_path)