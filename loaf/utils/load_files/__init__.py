from .file_ini import load_file_ini
from .file_sqlite import load_file_sqlite

def load_file(creds, file_path):
    if file_path[-4:] == ".ini":
        return load_file_ini(file_path, creds)
    if file_path[-3:] == ".db":
        return load_file_sqlite(file_path, creds)
    raise ValueError("Invalid file type or path.")
    
