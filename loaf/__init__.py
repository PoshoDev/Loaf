from .utils import CursorTypes, DatabaseTypes


class Loaf:
    def __init__(
        self,
        url: str = None,
        file: str = None,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        database: str = None,
        cursor_type: CursorTypes = CursorTypes.DICTIONARY,
        database_type: DatabaseTypes = DatabaseTypes.MYSQL,
        rollback_on_error: bool = True
    ):
        pass