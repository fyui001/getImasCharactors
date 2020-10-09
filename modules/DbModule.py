import mysql.connector as connector
import configparser
import os

class DbModule:

    def __db_connect(self):
        base = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.normpath(os.path.join(base, '../'))
        conf = configparser.ConfigParser()
        conf.read(conf_path+'/config/dbconfig.ini', encoding='utf-8')
        try:
            db = connector.connect(
                user = conf['DEFAULT']['USER'],
                passwd = conf['DEFAULT']['PASSWD'],
                host = conf['DEFAULT']['HOST'],
                db = conf['DEFAULT']['DATA_BASE']
            )
            return db
        except Exception as e:
            print(e)
            raise

    def table_check(self, table_name: str):
        cnx = self.__db_connect()
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

    def get(self, table_name: str):
        self.table_check(table_name)
        sql = 'SELECT name FROM {table_name}'.format(table_name=table_name)
        result = []
        cnx = self.__db_connect()
        cur = cnx.cursor()
        try:
            cur.execute(sql)
            for row in cur.fetchall():
                result.append(row[0])
            return result
        except:
            raise

    def truncate(self, table_name: str):
        sql = 'TRUNCATE TABLE `{table_name}`;'.format(table_name=table_name)
        cnx = self.__db_connect()
        cur = cnx.cursor()
        try:
            cur.execute(sql)
        except:
            raise

    def insert(self, sql: str):
        cnx = self.__db_connect()
        cur = cnx.cursor()

        try:
            cur.execute(sql)
            cnx.commit()
        except:
            cnx.rollback()
            raise
