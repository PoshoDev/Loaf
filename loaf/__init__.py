# A Python module for effortless database usage.

import pymysql, psycopg2, psycopg2.extras, sqlite3, datetime, socket, configparser

cursors = ["DEFAULT", "DICTIONARY"]
modes = ["MySQL", "PostgreSQL", "SQLite"]
defaults = {
    "host": socket.gethostbyname(socket.gethostname()),
    "port": 80, # Default XAMPP Apache server port.
    "user": "root",
    "pasw": "",
    "db": None,
    "cursor": cursors[0],
    "mode": modes[0]
}

# The Loaf class. Used to hold connections and other data in a single object.
class Loaf:
    def __init__(self, file=None, host=None, port=None, user=None, pasw=None, db=None,
                 cursor=None, mode=None):
        # If a file is specified, use it.
        if file is not None:
            # Creating from an INI file.
            if file[-4:] == ".ini":
                config = configparser.ConfigParser()
                config.read(file)
                sect = "DATABASE"
                section = config[sect]
                self.host = section["host"] if config.has_option(sect, "host") else defaults["host"]
                self.port = int(section["port"]) if config.has_option(sect, "port") else defaults["port"]
                self.user = section["user"] if config.has_option(sect, "user") else defaults["user"]
                self.pasw = section["pasw"] if config.has_option(sect, "pasw") else defaults["pasw"]
                self.db = section["db"] if config.has_option(sect, "db") else defaults["db"]
                self.cursorType = section["cursor"] if config.has_option(sect, "cursor") else defaults["cursor"]
                self.mode = section["mode"] if config.has_option(sect, "mode") else defaults["mode"]
            # Creating from a DB file
            elif file[-3:] == ".db":
                self.mode = "SQLite"
                self.db = file
                self.cursorType = cursor if cursor is not None else defaults["cursor"]
            else:
                raise Exception("Invalid file type.")
        # If no file is specified, use the arguments.
        else:
            self.host = host if host is not None else defaults["host"]
            self.port = port if port is not None else defaults["port"]
            self.user = user if user is not None else defaults["user"]
            self.pasw = pasw if pasw is not None else defaults["pasw"]
            self.db = db if db is not None else defaults["db"]
            self.cursorType = cursor if cursor is not None else defaults["cursor"]
            self.mode = mode if mode is not None else defaults["mode"]
        # Sanity checks.
        if self.mode not in modes:
            raise Exception(f"Invalid mode. Available modes: {modes}")
        if self.cursorType not in cursors:
            raise Exception(f"Invalid cursor type. Available types: {cursors}")
        # Create the connection.
        self.conn = self.createConnection(self)
        # Create the cursor.
        self.cursor = self.createCursor(self)

    # Creates a connection.
    def createConnection(self):
        if self.mode == "MySQL":
            return pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        password=self.pasw, db=self.db)
        elif self.mode == "PostgreSQL":
            return psycopg2.connect(host=self.host, port=self.port, user=self.user,
                                         password=self.pasw, database=self.db)
        elif self.mode == "SQLite":
            return sqlite3.connect(self.db)
        raise Exception("Invalid mode.")

    # Creates a cursor.
    def createCursor(self):
        if self.mode == "MySQL":
            if self.cursorType == "DEFAULT":
                return self.conn.cursor()
            elif self.cursorType == "DICTIONARY":
                return self.conn.cursor(pymysql.cursors.DictCursor)
        elif self.mode == "PostgreSQL":
            if self.cursorType == "DEFAULT":
                return self.conn.cursor()
            elif self.cursorType == "DICTIONARY":
                return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        elif self.mode == "SQLite":
            if self.cursorType == "DEFAULT":
                return self.conn.cursor()
            elif self.cursorType == "DICTIONARY":
                return self.conn.cursor() # SQLite doesn't support dictionaries?
        raise Exception("Invalid cursor type.")



    

