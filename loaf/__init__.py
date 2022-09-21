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
    "mode": modes[0],
    "rollback_on_error": True
}

# The Loaf class. Used to hold connections and other data in a single object.
class Loaf:
    def __init__(self, file=None, host=None, port=None, user=None, pasw=None, db=None,
                 cursor=None, mode=None, rollback_on_error=None):
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
                self.rollback_on_error = section["rollback_on_error"] if config.has_option(sect, "rollback_on_error") else defaults["rollback_on_error"]
            # Creating from a DB file
            elif file[-3:] == ".db":
                self.mode = "SQLite"
                self.db = file
                self.cursorType = cursor if cursor is not None else defaults["cursor"]
                self.rollback_on_error = rollback_on_error if rollback_on_error is not None else defaults["rollback_on_error"]
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
            self.rollback_on_error = rollback_on_error if rollback_on_error is not None else defaults["rollback_on_error"]
        # Sanity checks.
        if self.mode not in modes:
            raise Exception(f"Invalid mode. Available modes: {modes}")
        if self.cursorType not in cursors:
            raise Exception(f"Invalid cursor type. Available types: {cursors}")
        # Create the connection.
        self.conn = self.createConnection()
        # Create the cursor.
        self.cursor = self.createCursor()

    # Closes the connection.
    def __delete__(self):
        self.conn.close()

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

    # A query. If the argument is a string, it will be executed as a query. If the file argument is used, it will load the query string from a file.
    def query(self, query="", file=None, rollback_on_error=None):
        # Getting the rollback.
        rollback_on_error = rollback_on_error if rollback_on_error is not None else self.rollback_on_error
        # If a file is specified, use it.
        if file is not None:
            with open(file, "r") as f:
                query = f.read()
        # Sanity check.
        if query == "":
            raise Exception("No query specified.")
        # Execute the query.
        try:
            self.cursor.execute(query)
        except Exception as e:
            if rollback_on_error:
                self.conn.rollback()
            raise e
        else:
            self.conn.commit()
        # Return the result.
        return self.cursor.fetchall()

    # Performs multiple queries at once. The argument is a list of queries. If the file argument is True, it will load the query strings from files.
    def multi(self, queries=[], files=False, rollback_on_error=None):
        # Getting the rollback.
        rollback_on_error = rollback_on_error if rollback_on_error is not None else self.rollback_on_error
        # If a file is specified, use it.
        if files:
            for i in range(len(queries)):
                with open(queries[i], "r") as f:
                    queries[i] = f.read()
        # Sanity check.
        if queries == []:
            raise Exception("No queries specified.")
        # Execute the queries.
        results = []
        try:
            for query in queries:
                self.cursor.execute(query)
                results.append(self.cursor.fetchall())
                if not rollback_on_error:
                    self.conn.commit()
        except Exception as e:
            if rollback_on_error:
                self.conn.rollback()
            raise e
        else:
            if rollback_on_error:
                self.conn.commit()
        # Return the results.
        return results

    # Calls a stored procedure. The arguments are the name of the procedure and a list of arguments.
    def call(self, procedure, args=[], rollback_on_error=None):
        # Getting the rollback.
        rollback_on_error = rollback_on_error if rollback_on_error is not None else self.rollback_on_error
        # Sanity check.
        if procedure == "":
            raise Exception("No procedure specified.")
        # Execute the procedure.
        try:
            self.cursor.callproc(procedure, args)
        except Exception as e:
            if rollback_on_error:
                self.conn.rollback()
            raise e
        else:
            self.conn.commit()
        # Return the result.
        return self.cursor.fetchall()

    ### EASY FUNCTIONS ###

    # A quick SELECT query.
    def select(self, select, fromm="", where="", order="", limit=""):
        # Sanity check.
        if select == "":
            raise Exception("No SELECT specified.")
        # First fabricate the query.
        query = f"SELECT {select}"
        query += f" FROM {fromm}" if fromm != "" else ""
        query += f" WHERE {where}" if where != "" else ""
        query += f" ORDER BY {order}" if order != "" else ""
        query += f" LIMIT {limit}" if limit != "" else ""
        query += ";"
        # Execute the query.
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # A quick INSERT-INTO-VALUES query. The 'into' argument can be a string or a list of strings. The 'values' argument can be a string or a list of strings. If the 'values' argument is a list, it must be the same length as the 'into' argument.
    def insert(self, into, values, rollback_on_error=None):
        # Getting the rollback.
        rollback_on_error = rollback_on_error if rollback_on_error is not None else self.rollback_on_error
        # Sanity check.
        if into == "" or into == []:
            raise Exception("No INTO specified.")
        if values == "" or values == []:
            raise Exception("No VALUES specified.")
        # First fabricate the query string.
        if type(into) == list:
            if type(values) == list:
                if len(into) != len(values):
                    raise Exception("The INTO and VALUES must be the same amount.")
                into = ", ".join(into)
                values = ", ".join(values)
            else:
                into = ", ".join(into)
        else:
            if type(values) == list:
                values = ", ".join(values)
        # Execute the query.
        try:
            self.cursor.execute(f"INSERT INTO {into} VALUES ({values})")
        except Exception as e:
            if rollback_on_error:
                self.conn.rollback()
            raise e
        else:
            self.conn.commit()

    # Get all values from a table.
    def all(self, table):
        # Sanity check.
        if table == "":
            raise Exception("No table specified.")
        # Execute the query.
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()

    ### DATABASE STATUS FUNCTIONS ###

    # Get the database's current date.
    def currentDate(self):
        if self.mode == "MySQL":
            self.cursor.execute("SELECT CURDATE();")
        elif self.mode == "PostgreSQL":
            self.cursor.execute("SELECT CURRENT_DATE;")
        elif self.mode == "SQLite":
            self.cursor.execute("SELECT DATE('now');")
        else:
            raise Exception("Invalid mode.")
        return self.cursor.fetchall()[0][0]

    # Get the database's current time.
    def currentTime(self):
        if self.mode == "MySQL":
            self.cursor.execute("SELECT CURTIME();")
        elif self.mode == "PostgreSQL":
            self.cursor.execute("SELECT CURRENT_TIME;")
        elif self.mode == "SQLite":
            self.cursor.execute("SELECT TIME('now');")
        else:
            raise Exception("Invalid mode.")
        return self.cursor.fetchall()[0][0]

    # Get the database's current date and time.
    def currentDateTime(self):
        if self.mode == "MySQL":
            self.cursor.execute("SELECT NOW();")
        elif self.mode == "PostgreSQL":
            self.cursor.execute("SELECT CURRENT_TIMESTAMP;")
        elif self.mode == "SQLite":
            self.cursor.execute("SELECT DATETIME('now');")
        else:
            raise Exception("Invalid mode.")
        return self.cursor.fetchall()[0][0]

    # Get the database's current timestamp.
    def currentTimestamp(self):
        if self.mode == "MySQL":
            self.cursor.execute("SELECT UNIX_TIMESTAMP();")
        elif self.mode == "PostgreSQL":
            self.cursor.execute("SELECT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP);")
        elif self.mode == "SQLite":
            self.cursor.execute("SELECT STRFTIME('%s', 'now');")
        else:
            raise Exception("Invalid mode.")
        return self.cursor.fetchall()[0][0]


### UTILITIES ###

# Forces the current value to be parsed into a "NULL" string if applies. Otherwise, it cleans up the value.
def parse(value):
    if value in [None, "", "NULL"]:
        return "NULL"
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    return "'" + str(value).replace("'", "''") + "'"
