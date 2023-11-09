from ..database_types import DatabaseTypes
from ..creds import Creds


def load_file_sqlite(file_path, creds: Creds):
    creds.database_type = DatabaseTypes.SQLITE
    creds.database = file_path
    return creds
