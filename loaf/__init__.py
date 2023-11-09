from .utils import (Creds, CursorTypes, DatabaseTypes, DefaultConfig,
                    create_connection_and_cursor)


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
        self.creds = Creds(
            url=url,
            file_path=file_path,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursor_type=cursor_type,
            database_type=database_type,
            rollback_on_error=rollback_on_error
        )
        self.refresh()

    def __del__(self):
        self.conn.close()

    def refresh(self):
        self.connection, self.cursor = \
            create_connection_and_cursor(self.creds)
        
    def query(
        self,
        query: str,
        file_path: str = None,
        commit: bool = True,
        rollback_on_error: bool = None
    ):
        # Getting the rollback-on-error.
        rollback_on_error = rollback_on_error \
            if rollback_on_error is not None else self.creds.rollback_on_error
        # If a file is specified, use it.

    
        
    

    
    
    