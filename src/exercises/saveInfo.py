from src.exercises.logUtil import log as logging

import pymysql
import yaml


class SaveMap:
    host = None
    user = None
    password = None
    port = 3306
    database = 'ehx'
    map_table_name = 'user_work_map'
    ans_table_name = 'ans_tb'
    db = None

    def __init__(self):
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
        self.host = config['database']['host']
        self.user = config['database']['user']
        self.password = config['database']['password']
        self.port = config['database']['port']
        self.database = config['database']['database']
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port,
                                  db=self.database)

    def select(self, user):
        select_sql = "select * from user_work_map where user = '" + str(user) + "'"
        cursor = self.db.cursor()
        cursor.execute(select_sql)
        return cursor.fetchall()

    def select_ans_by_eid(self, eid):
        select_sql = 'select * from ans_tb where eid = ' + str(eid)
        cursor = self.db.cursor()
        cursor.execute(select_sql)
        return cursor.fetchone()

    def is_in(self, user, eid):
        select_sql = "select * from user_work_map where eid = " + str(eid) + " and user = '" + str(user) + "'"
        cursor = self.db.cursor()
        cursor.execute(select_sql)
        return True if len(cursor.fetchall()) > 0 else False

    def insert(self, user, eid, seid):
        insert_sql = 'insert into user_work_map(user, eid, seid) values(%s, %s, %s)'
        cursor = self.db.cursor()
        try:
            cursor.execute(insert_sql, (user, str(eid), str(seid)))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def ans_is_in(self, eid):
        select_sql = "select * from ans_tb where eid = " + str(eid)
        cursor = self.db.cursor()
        cursor.execute(select_sql)
        return True if len(cursor.fetchall()) > 0 else False

    def insert_ans(self, eid, ans_json):
        logging.info("saving " + str(ans_json))
        insert_sql = 'insert into ans_tb(eid, ans) values(%s, %s)'
        cursor = self.db.cursor()
        try:
            cursor.execute(insert_sql, (str(eid), str(ans_json)))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False


if __name__ == '__main__':
    obj = SaveMap()
    print(len(obj.select('pioneer')))
    # print(obj.insert("test", 292246, 6822074))
    # print(obj.is_in('test', 292362))
    # print(obj.is_in(292025))
