from .keeper import status
'''
获取seid
'''


class Getter:
    base_url = "https://www.ehuixue.cn/index/study/joinquiz?eid="

    def __init__(self, session_name):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'accept': '*/*'
        }
        self.session = status["session_" + str(session_name)]

    def get_by_eid(self, eid):
        url = self.base_url + str(eid)
        try:
            r = self.session.get(url=url, headers=self.headers)
            print(r.json())
            return r.json().get('data').get('seid')
        except:
            return None


if __name__ == '__main__':
    getter = Getter()
    eid = 292251
    print(getter.get_by_eid(eid))
