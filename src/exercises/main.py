import random
from src.exercises import saveInfo, getSeid, finishWork, parseQuiz, ckGetter
from src.exercises.logUtil import log as logging
import time
import yaml


def save_map(file, name):
    with open(file, encoding='utf-8') as f:
        config = yaml.safe_load(f)
        config = config
    start_eid = config['exercise']['start_eid']
    end_eid = config['exercise']['end_eid']
    client = saveInfo.SaveMap()
    get_er = getSeid.Getter()
    sleep_time = 10
    for eid in range(start_eid, end_eid + 1):
        if client.is_in(name, eid):
            logging.info(str(eid) + "  " + str(name) + "已获取过seid...")
            continue

        # 增加等待时间，模拟人类行为
        logging.info("随机等待1-2分钟，再开始获取试题" + str(sleep_time) + "s...")
        time.sleep(sleep_time)
        seid = get_er.get_by_eid(eid)

        if not seid:
            # 平台限制，已经作答完的试题无法再次获取seid
            logging.info(f"获取{name} {eid} 的seid失败, 也许已经完成了...")
            sleep_time = 10
            continue
        logging.debug(seid)
        # time.sleep(5)
        result = client.insert(name, eid, seid)
        logging.info("保存" + str(seid) + "结果：" + str(result))
        sleep_time = random.uniform(60, 120)
        time.sleep(13)


def pioneer_get_map(config):
    ck_getter = ckGetter.CkGetter()
    name, pwd = ck_getter.get_account('pioneer', config)
    ck_getter.post_login(name, pwd)
    save_map(config, "pioneer")
    return ck_getter.session.cookies


def todo_get_map(config):
    ck_getter = ckGetter.CkGetter()
    name, pwd = ck_getter.get_account('todo_user', config)
    ck_getter.post_login(name, pwd)
    save_map(config, "todo_user")
    return ck_getter.session.cookies, str(name)


def main(config):
    logging.info("开始获取未完成试题...")
    pioneer_ck = pioneer_get_map(config)

    logging.info("开始准备正确答案...")
    pioneer_postman = finishWork.PostMan('pioneer')
    pioneer_postman.finish_all_work_with_mock()
    parser = parseQuiz.Paser()
    parser.ans_spider()
    logging.info("答案准备完成...")
    #
    logging.info("开始作答...")
    todo_ck, todo_name = todo_get_map(config)
    todo_postman = finishWork.PostMan(todo_name)
    todo_postman.finish_all_work_with_right_answer()
    logging.info("作答完成...")


if __name__ == '__main__':
    # 注意config 路径
    main("../../config.yaml")
