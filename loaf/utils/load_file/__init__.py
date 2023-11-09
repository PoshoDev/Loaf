from .file_ini import load_file_ini

def load_file(file_path):
    if file_path[-4:] == ".ini":
        return load_file_ini(file_path)
    
