from src.exercises.keeper import status
from src.exercises.config import config
from src.exercises.ckGetter import CkGetter
from src.exercises.saveInfo import Client

loger = None


class Helper:

    def __init__(self):
        self.session = status["session"]
        self.course_detail_url = "https://www.ehuixue.cn/index/study/directdetail"
        self.client = Client()

    def get_detail(self):
        cid = config["cid"]
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

            loger.debug(work_list)
            if self.client.insert_works(cid, cname, work_list):
                loger.info("保存作业信息成功")
            else:
                loger.error("保存作业信息失败")
        except:
            loger.error("获取课程内容发送错误")


if __name__ == "__main__":
    from logUtil import loger as logging
    loger = logging
    CkGetter().post_login("17198642616", "TANRUIKAI888", loger)
    helper = Helper()
    helper.get_detail()
