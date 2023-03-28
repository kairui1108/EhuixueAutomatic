import json
import yaml

from src.exercises import saveInfo, parseQuiz
from src.exercises.logUtil import log as logging
import random
import re
import time
import requests
from pyquery import PyQuery as pq


'''
负责根据试题构造随即答案或正确答案，并直接提交答案
'''


class PostMan:
    cookie = None
    headers = None
    user_name = None

    def __init__(self, cookie, user_name):
        self.user_name = user_name
        self.cookie = cookie
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'accept': '*/*',
            'Cookie': cookie
        }

    def get_mock(self, eid, seid):
        base_url = 'https://www.ehuixue.cn/index/study/quizscore.html?'
        url = base_url + 'eid=' + str(eid) + '&' + 'seid=' + str(seid)
        doc = pq(requests.get(url, headers=self.headers).text)
        mock = {}

        score = doc('div.score')
        if score:
            # 已答完
            logging.info(str(eid) + "已完成作答，成绩为：" + score.text() + "分")
            return mock

        for tb in doc('#examlist > table').items():
            type = tb('thead > tr > th').text()
            logging.info(type)
            qtype = None
            if '单选题' in type:
                qtype = 1
                logging.debug('这是单选题')
            elif '判断题' in type:
                qtype = 3
                logging.debug('这是判断题')
            elif '多选题' in type:
                qtype = 2
                logging.debug('这是多选题')
            questions = tb('tbody > tr')
            for question in questions.items():
                tb_child = question('td > table')
                qid = tb_child.attr('id')
                if qid:

                    qid = re.findall("\d+", qid)[0]
                    # print(qid)
                    answer = {}
                    if qtype == 3:
                        answer = {'ans': '1', 'qtype': str(qtype), 'qid': int(qid)}
                    else:
                        answer = {'ans': 'A', 'qtype': str(qtype), 'qid': int(qid)}
                    mock[qid] = answer
                    logging.info(answer)
                else:
                    continue

        return mock

    def post_answer(self, eid, seid, data):
        url = 'https://www.ehuixue.cn/index/study/examsheet'

        data = {
            "temp": 0,
            "eid": eid,
            "seid": seid,
            "answer": json.dumps(data)
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'accept': '*/*',
            'Cookie': self.cookie,
            'origin': 'https://www.ehuixue.cn',
            'referer': 'https://www.ehuixue.cn/index/study/quizscore.html?eid=' + str(eid) + '&seid=' + str(seid),
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        # print(data)
        resp = requests.post(url, data=data, headers=headers)
        # print(resp.status_code)
        logging.info(resp.text)

    def finish_single_work_with_mock(self, eid, seid):
        mock = self.get_mock(eid, seid)
        logging.debug(mock)
        sleep_time = random.uniform(10 + len(mock), 30)
        time.sleep(sleep_time)
        if not bool(mock):
            logging.info("获取假答案失败,题号： %s".format(str(eid)))
            return
        self.post_answer(eid, seid, mock)
        time.sleep(5)

    def finish_all_work_with_mock(self):
        if self.user_name != 'pioneer':
            # 防止误伤
            logging.error("用户名配置有误...")
            return
        for item in saveInfo.SaveMap().select(self.user_name):
            eid = item[1]
            seid = item[2]
            mock = self.get_mock(eid, seid)
            logging.debug(mock)
            if not bool(mock):
                time.sleep(2)
                continue
            sleep_time = random.uniform(1, 5)
            logging.info("获取数据完毕，随 只因 等待" + str(sleep_time) + "s...")
            time.sleep(sleep_time)
            self.post_answer(eid, seid, mock)
            time.sleep(2)

    def finish_all_work_with_right_answer(self):
        client = saveInfo.SaveMap()
        for item in client.select(self.user_name):
            eid = item[1]
            seid = item[2]
            # 判断是否已经作答过
            if parseQuiz.Paser(self.cookie).is_done(eid, seid):
                logging.info(str(eid) + "已经作答过了...")
                # 可持续发展，防止黑ip
                time.sleep(6)
                continue
            data = client.select_ans_by_eid(eid)
            if data is None:
                logging.error("eid为" + str(eid) + "的试题未找到正确的答案，需手动检查一下....")
                continue
            answer = json.loads(data[1])
            logging.info("eid: {" + str(eid) + "}，获取到答案: {" + str(data[1]) + "}")
            sleep_time = random.uniform(20 + len(answer), 50)
            logging.info("准备回答，随 只因 等待" + str(sleep_time) + "s...")
            time.sleep(sleep_time)
            self.post_answer(eid, seid, answer)
            time.sleep(6)


if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    cookie = config['user']['pioneer_cookie']
    postman = PostMan(cookie, 'pioneer')
    # postman.finish_all_work_with_mock()
    postman.finish_all_work_with_right_answer()
