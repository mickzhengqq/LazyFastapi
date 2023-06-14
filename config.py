import pymysql

def get_conn(db="test"):
    conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            passwd="123456",
            db=db,
            charset='utf8')    
    return conn

def get_engine():
    engine = "mysql+pymysql://root:123456@127.0.0.1:3306/test"
    return engine