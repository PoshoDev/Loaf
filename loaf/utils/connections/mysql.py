import pymysql

from ..creds import Creds
from ..cursor_types import CursorTypes


def create_connection_mysql(creds: Creds):
    return pymysql.connect(
        host=creds.host,
        port=creds.port,
        user=creds.user,
        password=creds.password,
        db=creds.database
    )

def create_cursor_mysql(creds: Creds, connection):
        match creds.cursor_type:
            case CursorTypes.MATRIX:
                return connection.cursor()
            case CursorTypes.DICTIONARY:
                import pymysql
                return connection.cursor(pymysql.cursors.DictCursor)
        raise ValueError("Invalid 'cursor_type'.")
    