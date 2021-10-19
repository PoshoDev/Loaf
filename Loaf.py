import pymysql, datetime, socket

host = socket.gethostbyname(socket.gethostname)
port = 80 # Default XAMPP Apache server port.
user = "root"
pasw = ""
db = None
creds = ""

def bake(host=host, port=port, user=user, pasw=pasw, db=db, creds=creds):
    return "lol"

# Easier on the eyes.
def call(func, *args):
    call = "CALL " + func + "("
    if len(args) > 0:
        for i in range(len(args)):
            call += (str(args[i]) if type(args[i])==type(1) else parseNull(args[i])) + (", " if i<len(args)-1 else ");")
    else: call += ");"
    q = query(call)
    return q[0][0] if len(q)==1 else q

# A query.
def query(query):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=pasw, db=db)
    conn_object = conn.cursor()
    conn_object.execute(query)
    str = conn_object.fetchall()
    conn.commit()
    conn.close()
    return str

def getToday():
    dat = datetime.date.today() + datetime.timedelta(days=1)
    return dat.strftime("%Y-%m-%d")

def getTomorrow():
    dat = datetime.date.today() + datetime.timedelta(days=1)
    return dat.strftime("%Y-%m-%d")

def parseNull(val):
    return "NULL" if val in ["", "NULL"] else "'"+val+"'"
