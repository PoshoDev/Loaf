import pymysql, datetime
import _creds

# Easier on the eyes.
def Call(func, *args):
    call = "CALL " + func + "("
    if len(args) > 0:
        for i in range(len(args)):
            call += (str(args[i]) if type(args[i])==type(1) else ParseNull(args[i])) + (", " if i<len(args)-1 else ");")
    else: call += ");"
    q = Query(call)
    return q[0][0] if len(q)==1 else q

# A query.
def Query(query):
    conn = pymysql.connect(host=_creds.host, port=_creds.port, user=_creds.user, passwd=_creds.pasw, db=_creds.data)
    conn_object = conn.cursor()
    conn_object.execute(query)
    str = conn_object.fetchall()
    conn.commit()
    conn.close()
    return str

def GetToday():
    dat = datetime.date.today() + datetime.timedelta(days=1)
    return dat.strftime("%Y-%m-%d")

def GetTomorrow():
    dat = datetime.date.today() + datetime.timedelta(days=1)
    return dat.strftime("%Y-%m-%d")

def ParseNull(val):
    return "NULL" if val in ["", "NULL"] else "'"+val+"'"
