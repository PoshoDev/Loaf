from ..creds import Creds
from ..database_types import DatabaseTypes
from .mysql import create_connection_mysql, create_cursor_mysql
from .postgresql import create_connection_postgresql, create_cursor_postgresql
from .sqlite import create_connection_sqlite, create_cursor_sqlite


def create_connection_and_cursor(creds: Creds):
    match creds.database_type:
        case DatabaseTypes.MYSQL:
            conn = create_connection_mysql(creds)
            return conn, create_cursor_mysql(creds, conn)
        case DatabaseTypes.POSTGRESQL:
            conn = create_connection_postgresql(creds)
            return conn, create_cursor_postgresql(creds, conn)
        case DatabaseTypes.SQLITE:
            conn = create_connection_sqlite(creds)
            return conn, create_cursor_sqlite(creds, conn)
    raise ValueError("Invalid 'database_type'.")