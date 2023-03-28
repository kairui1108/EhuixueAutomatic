import random
import sys

from src.exercises import saveInfo, getSeid, finishWork
from src.exercises.logUtil import log as logging
import time


import yaml


def pioneer_get_map():
    config, pioneer_cookie = get_pioneer()
    if pioneer_cookie is None:
        logging.error("请在配置文件添加pioneer_cookie....")
        return
    save_map(config, "pioneer", pioneer_cookie)


def get_pioneer():
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    pioneer_cookie = config['user']['pioneer_cookie']
    return config, pioneer_cookie


def todo_get_map():
    config, todo_user, todo_user_cookie = get_user_info()
    if todo_user_cookie is None:
        logging.info("请在配置文件添加todo_user_cookie....")
        return
    save_map(config, todo_user, todo_user_cookie)


def get_user_info():
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    todo_user = config['user']['todo_user_name']
    todo_user_cookie = config['user']['todo_user_cookie']
    return config, todo_user, todo_user_cookie


def save_map(config, todo_user, todo_user_cookie):
    start_eid = config['user']['start_eid']
    end_eid = config['user']['end_eid']
    client = saveInfo.SaveMap()
    get_er = getSeid.Getter(todo_user_cookie)
    sleep_time = 10
    for eid in range(start_eid, end_eid + 1):
        if client.is_in(todo_user, eid):
            logging.info(str(eid) + "  " + todo_user + "已获取过seid...")
            continue

        # 增加等待时间，模拟人类行为, 非小白鼠账号记得打开注释
        logging.info("随机等待1-2分钟，再开始获取试题" + str(sleep_time) + "s...")
        time.sleep(sleep_time)
        # time.sleep(6)
        seid = get_er.get_by_eid(eid)

        if not seid:
            # 平台限制，已经作答完的试题无法再次获取seid
            logging.info("获取" + todo_user + str(eid) + "的seid失败, 也许已经完成了...")
            sleep_time = 10
            continue
        logging.debug(seid)
        # time.sleep(5)
        result = client.insert(todo_user, eid, seid)
        logging.info("保存" + str(seid) + "结果：" + str(result))
        sleep_time = random.uniform(60, 120)
        time.sleep(13)


def check_ck(cookie):
    pass


def main():
    logging.info("开始获取未完成试题...")
    # pioneer_get_map()
    todo_get_map()

    logging.info("开始准备正确答案...")
    # config, pioneer_cookie = get_pioneer()
    # pioneer_postman = finishWork.PostMan(pioneer_cookie, 'pioneer')
    # pioneer_postman.finish_all_work_with_mock()
    # parser = parseQuiz.Paser(pioneer_cookie)
    # parser.ans_spider()
    logging.info("答案准备完成...")
    #
    logging.info("开始作答...")
    config, todo_user, todo_user_cookie = get_user_info()
    if todo_user_cookie is None:
        logging.error("请在配置文件添加todo_user_cookie....")
        sys.exit()
    todo_postman = finishWork.PostMan(todo_user_cookie, todo_user)
    todo_postman.finish_all_work_with_right_answer()
    logging.info("作答完成...")


if __name__ == '__main__':
    # 注意config 路径
    main()
