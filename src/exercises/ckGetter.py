import requests
from .config import config
from .keeper import status


class CkGetter:

    def __init__(self, name, pwd, logging):
        self.session = requests.session()
        self.config = config
        self.name = name
        self.pwd = pwd
        self.logging = logging

    def post_login(self, session_name):
        login_url = "https://www.ehuixue.cn/index/login/checklogin"
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.ehuixue.cn'
        }
        body = {
            'type': 1,
            'account': self.name,
            'pwd': self.pwd,
            'code': None,
            'cancelflag': 0
        }
        res = self.session.post(url=login_url, headers=header, data=body)

        r = res.json()
        if r['status'] == 100:
            self.logging.info("模拟登录成功")
            status["session_" + str(session_name)] = self.session
            return self.session
        else:
            self.logging.error(r['msg'])
            raise Exception("登录失败")

    def get_study_course(self):
        url = "https://www.ehuixue.cn/index/Personal/getstudycourse"
        data = {
            'type': 1,
            'active': 'course'
        }
        res = self.session.post(url=url, data=data)
        print(res.status_code)
        print(res.json())


if __name__ == '__main__':
    from logUtil import loger
    uname = config["pioneer"]['phone']
    pwd = config["pioneer"]['pwd']
    getter = CkGetter(uname, pwd, loger)
    getter.post_login("pioneer")
    getter.get_study_course()
