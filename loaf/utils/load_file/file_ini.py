from configparser import ConfigParser
from ..default_config import DefaultConfig

def load_file_ini(file_path):
    config = ConfigParser()
    config.read(file_path)
    sect = "DATABASE"

    def get_option(option, default):
        return config.get(sect, option, fallback=default)
    
    return {
        'host': get_option("host", DefaultConfig.HOST),
        'port': int(get_option("port", DefaultConfig.PORT)),
        'user': get_option("user", DefaultConfig.USER),
        'password': get_option("pasw", DefaultConfig.PASSWORD),
        'database': get_option("db", DefaultConfig.DATABASE),
        'cursor_type': get_option("cursor", DefaultConfig.CURSOR_TYPE),
        'database_type': get_option("mode", DefaultConfig.DATABASE_TYPE),
        'rollback_on_error': get_option("rollback_on_error", DefaultConfig.ROLLBACK_ON_ERROR)
    }
