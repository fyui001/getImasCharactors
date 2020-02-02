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

def table_check(table_name):
    cnx = connect()
    cur = cnx.cursor()
    cur.execute("SHOW TABLES LIKE '{table_name}'".format(table_name=table_name))
    tables = cur.fetchall()
    if not tables:
        cur.execute("CREATE TABLE `{table_name}` ("
            "`id` int(11) NOT NULL AUTO_INCREMENT,"
            "`name` varchar(255) NOT NULL DEFAULT '',"
            "`name_kana` varchar(255) NOT NULL DEFAULT '',"
            "`age` int(11) UNSIGNED NOT NULL DEFAULT 0,"
            "`bust` float UNSIGNED NOT NULL DEFAULT 0,"
            "`hip` float UNSIGNED NOT NULL DEFAULT 0,"
            "`waist` float UNSIGNED NOT NULL DEFAULT 0,"
            "`color` varchar(40) NOT NULL DEFAULT '',"
            "`voice_actor` varchar(255) NOT NULL DEFAULT '',"
            "`title` varchar(50) NOT NULL DEFAULT '',"
            "PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4".format(table_name=table_name)
            )
        print('テーブルが存在しないので新しく作成')

def get(table_name):
    table_check(table_name)
    sql = 'SELECT name FROM {table_name}'.format(table_name=table_name)
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

def truncate(table_name):
    sql = 'TRUNCATE TABLE `{table_name}`;'.format(table_name=table_name)
    cnx = connect()
    cur = cnx.cursor()
    try:
        cur.execute(sql)
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
