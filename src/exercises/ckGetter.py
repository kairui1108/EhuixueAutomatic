import requests
import yaml
from .keeper import status


class CkGetter:

    def __init__(self):
        self.session = requests.session()
        self.config = None

    def get_account(self, name, config):
        with open(config, encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self.config = config
        uname = config[name]['name']
        pwd = config[name]['pwd']
        return uname, pwd

    def post_login(self, name, pwd):
        login_url = "https://www.ehuixue.cn/index/login/checklogin"
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.ehuixue.cn'
        }
        body = {
            'type': 1,
            'account': name,
            'pwd': pwd,
            'code': None,
            'cancelflag': 0
        }
        res = self.session.post(url=login_url, headers=header, data=body)
        if res.status_code == 200:
            status["session"] = self.session
            return self.session
        else:
            raise Exception("登录失败,未知错误")

    def get_study_course(self, cookie):
        url = "https://www.ehuixue.cn/index/Personal/getstudycourse"
        data = {
            'type': 1,
            'active': 'course'
        }
        res = self.session.post(url=url, data=data)
        print(res.status_code)
        print(res.json())


if __name__ == '__main__':
    getter = CkGetter()
    uname, pwd = getter.get_account("todo_user", "../../config.yaml")
    ck = getter.post_login(uname, pwd)
    print(ck)
    getter.get_study_course(ck)
