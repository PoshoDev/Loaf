from configparser import ConfigParser
from ..default_config import DefaultConfig
from ..creds import Creds

def load_file_ini(file_path, creds):
    config = ConfigParser()
    config.read(file_path)
    sect = "DATABASE"

    if config.has_option(sect, "host"):
        creds.host = config.get(sect, "host")
    if config.has_option(sect, "port"):
        creds.port = int(config.get(sect, "port"))
    if config.has_option(sect, "user"):
        creds.user = config.get(sect, "user")
    if config.has_option(sect, "pasw"):
        creds.password = config.get(sect, "pasw")
    if config.has_option(sect, "db"):
        creds.database = config.get(sect, "db")
    if config.has_option(sect, "cursor"):
        creds.cursor_type = config.get(sect, "cursor")
    if config.has_option(sect, "mode"):
        creds.database_type = config.get(sect, "mode")
    if config.has_option(sect, "rollback_on_error"):
        creds.rollback_on_error = config.getboolean(sect, "rollback_on_error")

    return creds
