import pymysql, psycopg2, datetime, socket, configparser

host_ = socket.gethostbyname(socket.gethostname())
port_ = 80 # Default XAMPP Apache server port.
user_ = "root"
pasw_ = ""
db_ = None
creds_ = ""
cursor_ = "DEFAULT"
mode_ = "MySQL"

# Make this differently, for the love of god!
def bake(host=host_, port=port_, user=user_, pasw=pasw_, db=db_, creds=creds_, cursor=cursor_, mode=mode_, file=None):
    global host_, port_, user_, pasw_, db_, creds_, cursor_, mode_
    if file is None:
        if host != "": host_=host
        if port != "": port_=port
        if user != "": user_=user
        if pasw != "": pasw_=pasw
        if db != "": db_=db
        if creds != "": creds_=creds
        if cursor != "": cursor_=cursor
        if mode != "": mode_=mode
    else:
        config = configparser.ConfigParser()
        config.read(file)
        section = config["DATABASE"]
        host_ = section["host"]
        port_ = int(section["port"])
        user_ = section["user"]
        pasw_ = section["pasw"]
        db_   = section["db"]
        mode_ = section["mode"]

# A query.
def query(query):
    if (mode_ == "MySQL"):
        conn = pymysql.connect(host=host_, port=port_, user=user_, passwd=pasw_, db=db_)
    elif (mode_ == "PostgreSQL"):
        conn = psycopg2.connect(host=host_, port=port_, user=user_, password=pasw_, database=db_)
    conn_object = conn.cursor(pymysql.cursors.DictCursor) if cursor_=="DICTIONARY" else conn.cursor()
    conn_object.execute(query)
    if conn_object.pgresult_ptr is not None:
        response = conn_object.fetchall()
    else:
        response = None
    conn.commit()
    conn.close()
    return response

# Test your connection with your database.
def test():
    try:
        if (mode_ == "MySQL"):
            conn = pymysql.connect(host=host_, port=port_, user=user_, passwd=pasw_, db=db_)
        elif (mode_ == "PostgreSQL"):
            conn = psycopg2.connect(host=host_, port=port_, user=user_, password=pasw_, database=db_)
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
