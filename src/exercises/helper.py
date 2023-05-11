from src.exercises.ckGetter import CkGetter
from src.exercises.saveInfo import Client
from src.exercises.config import config
from src.exercises.keeper import status

loger = None


class Helper:

    def __init__(self, session_name):
        self.session = None
        try:
            self.session = status["session_" + str(session_name)]
        except:
            self.session = None

        if self.session is None:
            self.login(session_name)
        else:
            res = self.session.post("https://www.ehuixue.cn/index/Personal/getmsgstatus")
            text = res.text
            if '<script>' in text:
                self.login(session_name)

        self.course_detail_url = "https://www.ehuixue.cn/index/study/directdetail"
        self.course_url = "https://www.ehuixue.cn/index/Personal/getstudycourse"
        self.client = Client()

    def login(self, name):
        if name == 'pioneer':
            phone = config['pioneer']['phone']
            pwd = config['pioneer']['pwd']
        else:
            phone = config['todo_user']['phone']
            pwd = config['todo_user']['pwd']
        CkGetter(phone, pwd, loger).post_login(name)
        self.session = status["session_" + str(name)]

    def get_detail(self, cid):
        data_json = {
            "cid": cid
        }
        try:
            work_list = []
            detail_res = self.session.post(url=self.course_detail_url, json=data_json).json()
            cname = detail_res["data"]["cbatch"]["course_name"]
            loger.info("课程名称： " + str(cname))
            course_part = detail_res["data"]["part"]
            for part in course_part:
                children = part["children"]
                if len(children) == 0:
                    # 试卷类型
                    eid = part["about_id"]
                    e_name = part["task_name"]
                    work = {
                        "eid": eid,
                        "name": e_name
                    }
                    work_list.append(work)
                    loger.info(str(eid) + " ==> " + e_name)
                    continue
                for task in children:
                    task_name = task["task_name"]
                    task_type = task["task_type"]
                    if task_type == "video":
                        task_leaf = task["leaf"]
                        for work in task_leaf:
                            eid = work["about_id"]
                            name = work["task_name"]
                            work = {
                                "eid": eid,
                                "name": name
                            }
                            work_list.append(work)
                            loger.info(str(eid) + " ==> " + name)

            # loger.debug(work_list)
            if self.client.insert_works(cid, cname, work_list):
                loger.info("保存作业信息成功")
                return work_list
            else:
                loger.error("保存作业信息失败")
        except:
            loger.error("获取课程内容出现错误")

    def get_study_course(self):
        data_json = {
            "active": "course",
            "limit": 10,
            "p": 1,
            "status": "1",
            "type": 2
        }
        try:
            res = self.session.post(url=self.course_url, json=data_json).json()
            all_course_list = res["data"]["info"]
            course_list = []
            for course in all_course_list:
                if course["cstatus"] == "已结束":
                    continue
                course_list.append(course)
            return course_list
        except:
            loger.error("获取课程信息失败")
            return None


if __name__ == "__main__":
    from logUtil import loger as logging
    loger = logging
    pass
