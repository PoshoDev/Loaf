import pymysql, psycopg2, psycopg2.extras, sqlite3, datetime, socket, configparser
from rich.table import Table
from rich import print as rprint

cursors = ["DICTIONARY", "DEFAULT"]
modes = ["MySQL", "PostgreSQL", "SQLite"]
removables = {
    "start": ['--sql', '--beginsql', '--begin-sql'],
    "end": ['--endsql', '--end-sql']
}

# The Loaf class. Used to hold connections and other data in a single object.
class Loaf:
    def __init__(self, file=None, host=None, port=None, user=None, pasw=None, db=None,
                 cursor=None, mode=None, rollback_on_error=None):
        # HACK: Define defaults here to avoid sockets error:
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
            # Creating from a .DB file
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
        # Create the connection and cursor.
        self.refresh()

    # Closes the connection.
    def __delete__(self):
        self.conn.close()

    # Refresh connection and cursor.
    def refresh(self):
        self.conn = self.createConnection()
        self.cursor = self.createCursor()

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
    def createCursor(self, cursorType=None):
        cursorType = cursorType if cursorType is not None else self.cursorType
        if self.mode == "MySQL":
            if cursorType == "DEFAULT":
                return self.conn.cursor()
            elif cursorType == "DICTIONARY":
                return self.conn.cursor(pymysql.cursors.DictCursor)
        elif self.mode == "PostgreSQL":
            if cursorType == "DEFAULT":
                return self.conn.cursor()
            elif cursorType == "DICTIONARY":
                return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        elif self.mode == "SQLite":
            if cursorType == "DEFAULT":
                return self.conn.cursor()
            elif cursorType == "DICTIONARY":
                return self.conn.cursor() # SQLite doesn't support dictionaries?
        raise Exception("Invalid cursor type.")

    # A query. If the argument is a string, it will be executed as a query. If the file argument is used, it will load the query string from a file.
    def query(self, query="", file=None, commit=True, rollback_on_error=None):
        # Getting the rollback.
        rollback_on_error = rollback_on_error if rollback_on_error is not None else self.rollback_on_error
        # If a file is specified, use it.
        if file is not None:
            with open(file, "r") as f:
                query = f.read()
        # Sanity check.
        if query == "":
            raise Exception("No query specified.")
        else:
            query = sParse(query)
        # Execute the query.
        try:
            self.refresh()
            self.cursor.execute(query)
        except Exception as e:
            if rollback_on_error:
                self.conn.rollback()
            raise e
        else:
            if commit:
                self.conn.commit()
        # Return the result.
        return self.cursor.fetchall()

    # Performs multiple queries at once. The argument is a list of queries. If the file argument is True, it will load the query strings from files.
    def multi(self, queries=[], files=False, commit=True, rollback_on_error=None):
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
            self.refresh()
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
            if commit:
                self.conn.commit()
        # Return the results.
        return results

    # Performs a query and returns the first result. It HAS to be done using the 'DEFAULT' cursor type.
    def single(self, query="", file=None, rollback_on_error=None):
        # Getting the rollback.
        rollback_on_error = rollback_on_error if rollback_on_error is not None else self.rollback_on_error
        # If a file is specified, use it.
        if file is not None:
            with open(file, "r") as f:
                query = f.read()
        # Sanity check.
        if query == "":
            raise Exception("No query specified.")
        else:
            query = sParse(query)
        # Execute the query.
        try:
            self.refresh()
            tempCursor = self.createCursor("DEFAULT")
            tempCursor.execute(query)
        except Exception as e:
            if rollback_on_error:
                self.conn.rollback()
            raise e
        else:
            self.conn.commit()
        # Return the result.
        try:
            return tempCursor.fetchall()[0][0]
        except:
            try:
                return tempCursor.fetchall()[0]
            except:
                return tempCursor.fetchall()

    # A simple commit.
    def commit(self):
        self.conn.commit()

    # Calls a stored procedure. The arguments are the name of the procedure and a list of arguments.
    def call(self, procedure, args=[], rollback_on_error=None):
        # Getting the rollback.
        rollback_on_error = rollback_on_error if rollback_on_error is not None else self.rollback_on_error
        # Sanity check.
        if procedure == "":
            raise Exception("No procedure specified.")
        # Execute the procedure.
        try:
            self.refresh()
            self.cursor.callproc(procedure, args)
        except Exception as e:
            if rollback_on_error:
                self.conn.rollback()
            raise e
        else:
            self.conn.commit()
        # Return the result.
        return self.cursor.fetchall()

    ### PRINT FUNCTIONS ###

    # Prints the result of a query as a rich table. The 'data' argument can be a tuple or a dictionary. 
    def print(self, data, title=None):
        if type(data) == dict:
            data = tuple(data.items())
        if type(data) == tuple:
            data = list(data)
        if type(data) == list:
            table = Table(title=title)
            if type(data[0]) == tuple:
                for i in range(len(data[0])):
                    table.add_column(data[0][i])
                for i in range(1, len(data)):
                    table.add_row(*data[i])
            elif type(data[0]) == dict:
                for i in data[0].keys():
                    table.add_column(i)
                for i in data:
                    values = []
                    for j in i.values():
                        values.append(tParse(j))
                    table.add_row(*values)
            rprint(table)
        else:
            raise Exception("Invalid data type.")

    ### EASY FUNCTIONS ###

    # A quick SELECT query.
    def select(self, select, fromm="", where="", order="", limit=""):
        # Sanity check.
        if select == "":
            raise Exception("No FROM specified.")
        # First fabricate the query.
        query = f"SELECT {select}"
        query += f" FROM {fromm}" if fromm != "" else ""
        query += f" WHERE {where}" if where != "" else ""
        query += f" ORDER BY {order}" if order != "" else ""
        query += f" LIMIT {limit}" if limit != "" else ""
        query += ";"
        # Execute the query.
        self.refresh()
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # A quick SELECT * FROM query.
    def selectAll(self, fromm="", where="", order="", limit=""):
        self.refresh()
        return self.select("*", fromm, where, order, limit)

    # A quick INSERT-INTO-VALUES query. The 'into' argument can be a string or a list of strings. The 'values' argument can be a string or a list of strings. If the 'values' argument is a list, it must be the same length as the 'into' argument.
    def insert(self, table, into, values, rollback_on_error=None):
        # Getting the rollback.
        rollback_on_error = rollback_on_error if rollback_on_error is not None else self.rollback_on_error
        # Sanity check.
        if into == "" or into == []:
            raise Exception("No INTO specified.")
        if values == "" or values == []:
            raise Exception("No VALUES specified.")
        # First fabricate the query string.
        if type(into) != type(values):
            raise Exception("The INTO and VALUES arguments must be of the same type.")
        if type(into) == str:
            finalInto = parse(into)
            finalValues = parse(values)
        elif type(into) == list:
            if len(into) != len(values):
                raise Exception("The INTO and VALUES arguments must be the same length.")
            finalInto = ""
            finalValues = ""
            for i in range(len(into)):
                finalInto += into[i] + ", "
                finalValues += parse(values[i]) + ", "
            finalInto = finalInto[:-2]
            finalValues = finalValues[:-2]
        else:
            raise Exception("Invalid INTO or VALUES type.")
        # Execute the query.
        try:
            self.refresh()
            self.cursor.execute(f"INSERT INTO {table} ({finalInto}) VALUES ({finalValues})")
        except Exception as e:
            if rollback_on_error:
                self.conn.rollback()
            raise e
        else:
            self.conn.commit()

    # A quick DELETE query.
    def delete(self, table, where=""):
        self.refresh()
        # Sanity check.
        if table == "":
            raise Exception("No table specified.")
        self.query(f"DELETE FROM {table} WHERE {where}")

    # A quick UPDATE query.
    def update(self, table, columns, values, where=""):
        # First fabricate the query string.
        if type(columns) != type(values):
            raise Exception("The COLUMNS and VALUES arguments must be of the same type.")
        if type(columns) == str:
            finalColumns = columns
            finalValues = parse(values)
        elif type(columns) == list:
            if len(columns) != len(values):
                raise Exception("The COLUMNS and VALUES arguments must be the same length.")
            setValues = ""
            for i in range(len(columns)):
                setValues += f"{columns[i]} = {parse(values[i])}, "
            setValues = setValues[:-2]
        else:
            raise Exception("Invalid COLUMNS or VALUES type.")
        self.query(f"UPDATE {table} SET {setValues} WHERE {where}")

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
    if isinstance(value, int):
        return str(value)
    if isinstance(value, datetime.date):
        return "'" + value.strftime("%Y-%m-%d") + "'"
    return "'" + str(value).replace("'", "''") + "'"

# Parses a value to a colored string to be used in tables.
def tParse(value):
    if value in [None, "", "NULL"]:
        return "[dim]NULL[/]"
    if isinstance(value, int):
        return "[magenta]" + str(value) + "[/]"
    if isinstance(value, datetime.date):
        return "[cyan]" + value.strftime("%Y-%m-%d") + "[/]"
    return "[green]'" + str(value).replace("'", "''") + "'[/]"

# Removes the "--sql" substring from the beginning of the value so that queries are compatible with VScode extensions like python-string-sql.
def sParse(value):
    for removable in removables["start"]:
        if value.startswith(removable):
            value = value[len(removable):]
            break
    for removable in removables["end"]:
        if value.endswith(removable):
            value = value[:-len(removable)]
            break
    return value