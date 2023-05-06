import random
from src.exercises import saveInfo, getSeid, finishWork, parseQuiz, ckGetter
from src.exercises.config import config
import time

log = None


def save_map(name):
    start_eid = config['exercise']['start_eid']
    end_eid = config['exercise']['end_eid']
    client = saveInfo.Client()
    get_er = getSeid.Getter()
    sleep_time = 10
    for eid in range(int(start_eid), int(end_eid) + 1):
        if client.is_in(name, eid):
            log.info(str(eid) + "  " + str(name) + "已获取过seid...")
            continue

        # 增加等待时间，模拟人类行为
        log.info("随机等待1-2分钟，再开始获取试题" + str(sleep_time) + "s...")
        time.sleep(sleep_time)
        seid = get_er.get_by_eid(eid)

        if not seid:
            # 平台限制，已经作答完的试题无法再次获取seid
            log.info(f"获取{name} {eid} 的seid失败, 也许已经完成了...")
            sleep_time = 10
            continue
        # log.debug(seid)
        # time.sleep(5)
        result = client.insert(name, eid, seid)
        log.info("保存" + str(eid) + "--" + str(seid) + "结果：" + str(result))
        sleep_time = random.uniform(60, 120)
        time.sleep(13)


def pioneer_get_map():
    ck_getter = ckGetter.CkGetter()
    name, pwd = ck_getter.get_account('pioneer')
    ck_getter.post_login(name, pwd, log)
    save_map("pioneer")
    return ck_getter.session.cookies


def todo_get_map():
    ck_getter = ckGetter.CkGetter()
    name, pwd = ck_getter.get_account('todo_user')
    ck_getter.post_login(name, pwd, log)
    save_map("todo_user")
    return ck_getter.session.cookies, str(name)


def main():
    get_ans()
    #
    run_post()


def run_post():
    log.info("开始作答...")
    todo_ck, todo_name = todo_get_map()
    todo_postman = finishWork.PostMan(todo_name)
    todo_postman.finish_all_work_with_right_answer()
    log.info("作答完成...")


def get_ans():
    log.info("开始获取未完成试题...")
    pioneer_get_map()
    log.info("开始准备正确答案...")
    finishWork.log = log
    pioneer_postman = finishWork.PostMan('pioneer')
    pioneer_postman.finish_all_work_with_mock()
    parseQuiz.log = log
    parser = parseQuiz.Paser()
    parser.ans_spider()
    log.info("答案准备完成...")


if __name__ == '__main__':
    from src.exercises.logUtil import log as logging
    log = logging
    # 注意config 路径
    main()
