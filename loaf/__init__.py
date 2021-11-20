import pymysql, datetime, socket

host_ = socket.gethostbyname(socket.gethostname())
port_ = 80 # Default XAMPP Apache server port.
user_ = "root"
pasw_ = ""
db_ = None
creds_ = ""

# Make this differently, for the love of god!
def bake(host=host_, port=port_, user=user_, pasw=pasw_, db=db_, creds=creds_):
    global host_, port_, user_, pasw_, db_, creds_
    if host != "": host_=host
    if port != "": port_=port
    if user != "": user_=user
    if pasw != "": pasw_=pasw
    if db != "": db_=db
    if creds != "": creds_=creds

# A query.
def query(query):
    conn = pymysql.connect(host=host_, port=port_, user=user_, passwd=pasw_, db=db_)
    conn_object = conn.cursor()
    conn_object.execute(query)
    str = conn_object.fetchall()
    conn.commit()
    conn.close()
    return str

# Call a stored procedure.
def call(func, *args):
    call = "CALL " + func + "("
    if len(args) > 0:
        for i in range(len(args)):
            call += (str(args[i]) if type(args[i])==type(1) else parseNull(args[i])) + (", " if i<len(args)-1 else ");")
    else: call += ");"
    q = query(call)
    return q[0][0] if (len(q)==1 and len(q[0])==1) else q

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
    return "NULL" if val in ["", "NULL"] else "'"+val+"'"
