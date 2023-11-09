import sqlite3

from ..creds import Creds
from ..cursor_types import CursorTypes


def create_connection_sqlite(creds: Creds):
    return sqlite3.connect(creds.database)

def create_cursor_sqlite(creds: Creds, connection):
    match creds.cursor_type:
        case CursorTypes.MATRIX:
            return connection.cursor()
        case CursorTypes.DICTIONARY:
            return connection.cursor() # SQLite doesn't support dictionaries?
    raise ValueError("Invalid 'cursor_type'.")