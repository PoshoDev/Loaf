import psycopg2
import psycopg2.extras

from ..creds import Creds
from ..cursor_types import CursorTypes


def create_connection_postgresql(creds: Creds):
    return psycopg2.connect(
        host=creds.host,
        port=creds.port,
        user=creds.user,
        password=creds.password,
        database=creds.database
    )

def create_cursor_postgresql(creds: Creds, connection):
    match creds.cursor_type:
        case CursorTypes.MATRIX:
            return connection.cursor()
        case CursorTypes.DICTIONARY:
            return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    raise ValueError("Invalid 'cursor_type'.")
    