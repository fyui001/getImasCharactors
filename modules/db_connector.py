from config import db_conf as db_conf
import mysql.connector as connector

def connect():
    try:
        db = connector.connect(
            user = db_conf.USER,
            passwd = db_conf.PASSWD,
            host = db_conf.HOST,
            db = db_conf.DATABESE
        )
        return db
    except Exception as e:
        print(e)

def get():
    sql = 'SELECT name FROM voice_actors'
    result = []
    cnx = connect()
    cur = cnx.cursor()
    try:
        cur.execute(sql)
        for row in cur.fetchall():
            result.append(row[0])
        return result
    except:
        raise

def insert(sql):
    cnx = connect()
    cur = cnx.cursor()

    try:
        cur.execute(sql)
        cnx.commit()
    except:
        cnx.rollback()
        raise
