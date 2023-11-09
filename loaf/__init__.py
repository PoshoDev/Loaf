from .utils import (Creds, CursorTypes, DatabaseTypes, DefaultConfig,
                    load_file, parse_sql_url)


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
        self.connection = self._create_connection()
        self.cursor = self._create_cursor()

    def _get_creds(url, file_path, creds):
        if url:
            return parse_sql_url(url, creds)
        if file_path:
            return load_file(file_path, creds)
        
    def _create_connection_and_cursor(self):
        match self.creds.database_type:
            case DatabaseTypes.MYSQL:
                self.connection = self._create_connection_mysql()
                self.cursor = self._create_cursor_mysql()
            case DatabaseTypes.POSTGRESQL:
                self.connection = self._create_connection_postgresql()
                self.cursor = self._create_cursor_postgresql()
            case DatabaseTypes.SQLITE:
                self.connection = self._create_connection_sqlite()
                self.cursor = self._create_cursor_sqlite()
        raise ValueError("Invalid 'database_type'.")

    def _create_connection_mysql(self):
        import pymysql
        return pymysql.connect(
            host=self.creds.host,
            port=self.creds.port,
            user=self.creds.user,
            password=self.creds.password,
            db=self.creds.database
        )
    
    def _create_connection_postgresql(self):
        import psycopg2
        return psycopg2.connect(
            host=self.creds.host,
            port=self.creds.port,
            user=self.creds.user,
            password=self.creds.password,
            database=self.creds.database
        )
    
    def _create_connection_sqlite(self):
        import sqlite3
        return sqlite3.connect(self.creds.database)

    def _create_cursor_mysql(self):
        match self.creds.cursor_type:
            case CursorTypes.MATRIX:
                return self.connection.cursor()
            case CursorTypes.DICTIONARY:
                import pymysql
                return self.connection.cursor(pymysql.cursors.DictCursor)
        raise ValueError("Invalid 'cursor_type'.")
    
    def _create_cursor_postgresql(self):
        match self.creds.cursor_type:
            case CursorTypes.MATRIX:
                return self.connection.cursor()
            case CursorTypes.DICTIONARY:
                import psycopg2.extras
                return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        raise ValueError("Invalid 'cursor_type'.")
    
    def _create_cursor_sqlite(self):
        match self.creds.cursor_type:
            case CursorTypes.MATRIX:
                return self.connection.cursor()
            case CursorTypes.DICTIONARY:
                return self.conn.cursor() # SQLite doesn't support dictionaries?
        raise ValueError("Invalid 'cursor_type'.")