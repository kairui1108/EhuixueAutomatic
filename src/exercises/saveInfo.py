from src.exercises.logUtil import loger as logging
import sqlite3


class Client:

    def __init__(self):
        self.db = sqlite3.connect('ehx.db')
        self.map_table_name = "user_work_map"
        self.ans_table_name = "ans_tb"
        self.work_table_name = "work_tb"
        self.create_map_table()
        self.create_ans_table()
        self.create_work_table()

    def create_map_table(self):
        c = self.db.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, user TEXT, eid INTEGER, seid INTEGER)'.format(
            self.map_table_name))
        self.db.commit()

    def create_ans_table(self):
        c = self.db.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, eid INTEGER, ans TEXT)'.format(self.ans_table_name))
        self.db.commit()

    def create_work_table(self):
        c = self.db.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, cid INTEGER, cname TEXT, works TEXT)'.format(
                self.work_table_name))
        self.db.commit()

    def select(self, user):
        select_sql = "select * from {} where user = ?".format(self.map_table_name)
        cursor = self.db.cursor()
        cursor.execute(select_sql, (user, ))
        return cursor.fetchall()

    def select_ans_by_eid(self, eid):
        select_sql = 'select * from {} where eid = '.format(self.ans_table_name)
        cursor = self.db.cursor()
        cursor.execute(select_sql, (eid, ))
        return cursor.fetchone()

    def is_in(self, user, eid):
        select_sql = "SELECT * FROM {} WHERE eid = ? AND user = ?".format(self.map_table_name)
        cursor = self.db.cursor()
        cursor.execute(select_sql, (eid, user))
        return True if len(cursor.fetchall()) > 0 else False

    def insert(self, user, eid, seid):
        insert_sql = "INSERT INTO {} (user, eid, seid) VALUES (?, ?, ?)".format(self.map_table_name)
        cursor = self.db.cursor()
        try:
            cursor.execute(insert_sql, (user, eid, seid))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def ans_is_in(self, eid):
        select_sql = "SELECT * FROM {} WHERE eid = ?".format(self.ans_table_name)
        cursor = self.db.cursor()
        cursor.execute(select_sql, (eid,))
        return True if len(cursor.fetchall()) > 0 else False

    def insert_ans(self, eid, ans_json):
        logging.info("saving " + str(ans_json))
        insert_sql = "INSERT INTO {} (eid, ans) VALUES (?, ?)".format(self.ans_table_name)
        cursor = self.db.cursor()
        try:
            cursor.execute(insert_sql, (eid, ans_json))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def insert_works(self, cid, cname, works):
        insert_sql = "INSERT INTO {} (cid, cname, works) VALUES (?, ?, ?)".format(self.work_table_name)
        cursor = self.db.cursor()
        try:
            cursor.execute(insert_sql, (cid, cname, str(works)))
            self.db.commit()
            return True
        except Exception as e:
            print("Error occurred: ", e)
            self.db.rollback()
            return False

    def get_works(self, cid):
        query_sql = "SELECT * FROM {} WHERE cid = ?".format(self.work_table_name)
        cursor = self.db.cursor()
        cursor.execute(query_sql, (str(cid), ))
        return cursor.fetchone()


if __name__ == '__main__':
    obj = Client()
    print(len(obj.select('pioneer')))
    # print(obj.insert("test", 292246, 6822074))
    # print(obj.is_in('test', 292362))
    # print(obj.is_in(292025))
    # print(obj.insert_works("1", "test", "test"))
    print(obj.get_works("39215"))
