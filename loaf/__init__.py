import pymysql, psycopg2, psycopg2.extras, datetime, socket, configparser

host_ = socket.gethostbyname(socket.gethostname())
port_ = 80 # Default XAMPP Apache server port.
user_ = "root"
pasw_ = ""
db_ = None
curs_ = "DEFAULT"
mode_ = "MySQL"

# Make this differently, for the love of god!
def bake(host=host_, port=port_, user=user_, pasw=pasw_, db=db_, cursor=curs_,
         mode=mode_, file=None):
    global host_, port_, user_, pasw_, db_, curs_, mode_
    if file is None:
        if host != "": host_=host
        if port != "": port_=port
        if user != "": user_=user
        if pasw != "": pasw_=pasw
        if db != "": db_=db
        if cursor != "": curs_=cursor
        if mode != "": mode_=mode
    else:
        config = configparser.ConfigParser()
        config.read(file)
        sect = "DATABASE"
        section = config[sect]
        if config.has_option(sect, "host"): host_ = section["host"]
        if config.has_option(sect, "port"): port_ = int(section["port"])
        if config.has_option(sect, "user"): user_ = section["user"]
        if config.has_option(sect, "pasw"): pasw_ = section["pasw"]
        if config.has_option(sect, "db"):   db_   = section["db"]
        if config.has_option(sect, "curs"): curs_ = section["curs"]
        if config.has_option(sect, "mode"): mode_ = section["mode"]

# A query.
def query(query):
    conn = get_connection()
    conn_object = get_connection_object(conn)
    conn_object.execute(query)
    if not mode_=="PostgreSQL" or conn_object.pgresult_ptr is not None:
        response = conn_object.fetchall()
    else:
        response = None
    conn.commit()
    conn.close()
    return response

# A way to use multiple queries.
def multi(queries):
    pass

def get_connection():
    if (mode_ == "PostgreSQL"):
        return psycopg2.connect(host=host_, port=port_, user=user_,
                                password=pasw_, database=db_)
    else: # MySQL (by Default)
        return pymysql.connect(host=host_, port=port_, user=user_,
                               passwd=pasw_, db=db_)

def get_connection_object(conn):
    # PostgreSQL
    if (mode_ == "PostgreSQL"):
        if curs_ == "DICTIONARY":
            return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            return conn.cursor()
    # MySQL (by Default)
    else:
        if curs_ == "DICTIONARY":
            return conn.cursor(pymysql.cursors.DictCursor)
        else:
            return conn.cursor()

# Test your connection with your database.
def test():
    try:
        get_connection()
        print(f"Successful connection at: {host_}")
    except Exception as ex:
        print(f"Connection error at: {host_}")
        print(ex)

# Call a stored procedure.
def call(func, *args):
    call = "CALL " + func + "("
    if len(args) > 0:
        for i in range(len(args)):
            call += (str(args[i]) if type(args[i])==type(1) else parseNull(args[i])) + (", " if i<len(args)-1 else ");")
    else: call += ");"
    q = query(call)
    return q[0][0] if (len(q)==1 and len(q[0])==1) else q

# Quick SELECT-FROM-WHERE
# /!\ Allow to pass lists too in the future.
def sfw(select, fromm="", where=""):
    query_str = f"SELECT {select} "
    if fromm:
        query_str += f"FROM {fromm} "
    if where:
        query_str += f"WHERE {where};"
    return query(query_str)

# Quick insert.
"""
def insert(table, cols=[], vals):
    call = f"INSERT INTO {table}"
    if len(cols):
        call += '('
        for col in cols:
            # INCOMPLETO!
"""

# Quick query.
def all(table):
    return query(f"SELECT * from {table};")

def getToday():
    dat = datetime.date.today() + datetime.timedelta(days=1)
    return dat.strftime("%Y-%m-%d")

def getTomorrow():
    dat = datetime.date.today() + datetime.timedelta(days=1)
    return dat.strftime("%Y-%m-%d")

def parseNull(val):
    if val in [None, "", "NULL"]:
        return "NULL"
    elif isinstance(val, datetime.date):
        return parseDate(val)
    else:
        return "'"+val+"'"

def parseDate(val):
    return val.strftime("%Y-%m-%d")

def lol():
    print("lol")
