from .utils import (Creds, CursorTypes, DatabaseTypes, DefaultConfig,
                    create_connection_and_cursor, load_file, parse_sql_url)


class Loaf:
    def __init__(
        self,
        url: str = None,
        file_path: str = None,
        host: str = DefaultConfig.HOST,
        port: int = DefaultConfig.PORT,
        user: str = DefaultConfig.USER,
        password: str = DefaultConfig.PASSWORD,
        database: str = DefaultConfig.DATABASE,
        cursor_type: CursorTypes = DefaultConfig.CURSOR_TYPE,
        database_type: DatabaseTypes = DefaultConfig.DATABASE_TYPE,
        rollback_on_error: bool = DefaultConfig.ROLLBACK_ON_ERROR
    ):
        self.creds = self._get_creds(
            url,
            file_path,
            Creds(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                cursor_type=cursor_type,
                database_type=database_type,
                rollback_on_error=rollback_on_error
            )
        )
        self.refresh()

    def __del__(self):
        self.conn.close()

    def refresh(self):
        self.connection, self.cursor = \
            create_connection_and_cursor(self.creds)

    def _get_creds(url, file_path, creds):
        if url:
            return parse_sql_url(url, creds)
        if file_path:
            return load_file(file_path, creds)
        
    

    
    
    