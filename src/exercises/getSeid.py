import requests

'''
获取seid
'''


class Getter:
    base_url = "https://www.ehuixue.cn/index/study/joinquiz?eid="
    cookie = ""
    headers = ""

    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'accept': '*/*',
            'Cookie': cookie
        }

    def get_by_eid(self, eid):
        url = self.base_url + str(eid)
        try:
            r = requests.get(url, headers=self.headers)
            return r.json().get('data').get('seid')
        except:
            return None


if __name__ == '__main__':
    cookie = ''
    getter = Getter(cookie)
    eid = 292251
    print(getter.get_by_eid(eid))
