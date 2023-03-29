import json
import random
import re
import time

from src.exercises import finishWork, saveInfo
from src.exercises.logUtil import log as logging
import requests
from pyquery import PyQuery as pq
import yaml

'''
负责解析考试页面，获取正确答案，并保存于数据库
'''


class Paser:
    cookie = None
    headers = None
    base_url = 'https://www.ehuixue.cn/index/study/quizscore.html?'
    undo_list = []

    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'accept': '*/*'
        }
        self.session = requests.session()

    def is_done(self, eid, seid):
        url = self.base_url + 'eid=' + str(eid) + '&' + 'seid=' + str(seid)
        doc = pq(self.session.get(url, headers=self.headers, cookies=self.cookie).text)
        score = doc('div.score')
        noscore = doc('div.noscore')
        if len(score) > 0 or len(noscore) > 0:
            return True
        return False

    def get_ans(self, eid, seid):
        url = self.base_url + 'eid=' + str(eid) + '&' + 'seid=' + str(seid)
        doc = pq(self.session.get(url, headers=self.headers, cookies=self.cookie).text)
        post_body = {}
        score = doc('div.score')
        if not score:
            # 未作答
            logging.info("eid为" + str(eid) + "的试题未作答, 开始作答...")
            postman = finishWork.PostMan(self.cookie)
            postman.finish_single_work_with_mock(eid, seid)
            # 平台限制，作答完后台批改答案需要一定时间，不能第一时间获取答案
            # return self.get_ans(eid, seid)
            # 后续等待重新获取答案
            self.undo_list.append((eid, seid))
            logging.info("undo_list: " + str(self.undo_list))
            return post_body
        for tb in doc('#examlist > table').items():
            questions = tb('tbody > tr')
            for question in questions.items():
                tb_child = question('td > table')
                qid = tb_child.attr('id')
                if qid:
                    logging.debug(qid)
                    qid = re.findall("\d+", qid)[0]
                for tr in question('td > table > tbody > tr').items():
                    text = tr('td > p').text()
                    box = tr('td.analysisbox')
                    if text:
                        # logging.debug(text)
                        pass
                    elif box:
                        ans = box('div .rightasweer').text()

                        answer = None
                        if ans == '正确':
                            answer = {'ans': '1', 'qtype': '3', 'qid': int(qid)}
                        elif ans == '错误':
                            answer = {'ans': '2', 'qtype': '3', 'qid': int(qid)}
                        else:
                            if len(ans.split(",")) == 1:
                                answer = {'ans': ans, 'qtype': '1', 'qid': int(qid)}
                            else:
                                answer = {'ans': ans, 'qtype': '2', 'qid': int(qid)}
                        logging.debug(str(answer))
                        post_body[qid] = answer
        return post_body

    def save_ans_into_db(self, client, eid, seid):
        if client.ans_is_in(eid):
            logging.info("eid为" + str(eid) + "的试题已存在...")
            return
        # 解析答案
        ans = self.get_ans(eid, seid)
        if not bool(ans):
            logging.error("eid=" + str(eid) + "的试题解析失败, 已添加到待办列表，等待重试...")
            return
        result = client.insert_ans(eid, json.dumps(ans))
        if result:
            logging.info("保存成功" + str(ans))
        else:
            logging.error("保存失败 " + str(eid) + ": " + str(ans))
        time.sleep(random.uniform(5, 15))

    def ans_spider(self):
        client = saveInfo.SaveMap()
        for item in client.select('pioneer'):
            eid = item[1]
            seid = item[2]
            self.save_ans_into_db(client, eid, seid)
        if len(self.undo_list) > 0:
            logging.info("等待网站后台批改答案后重试获取试题答案...")
            for item in self.undo_list:
                # (eid, seid)
                logging.info("等待5分钟...")
                time.sleep(300)
                eid = item[0]
                seid = item[1]
                self.save_ans_into_db(client, eid, seid)


if __name__ == '__main__':
    with open('../../config.yaml') as f:
        config = yaml.safe_load(f)
    cookie = config['user']['pioneer_cookie']
    parser = Paser(cookie)
    parser.ans_spider()
