import base64
import json
import threading
import time
import requests
import yaml
from selenium.common import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging = None


def init_browser_on_window():
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    return_browser = webdriver.Chrome(options=options)
    return_browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    return return_browser


def init_browser_on_window_with_no_head():
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    return_browser = webdriver.Chrome(chrome_options=options)
    return_browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    return return_browser


def init_browser_on_centos():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    return_browser = webdriver.Chrome(executable_path="/root/chrome/chromedriver", chrome_options=chrome_options)
    return_browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    return return_browser


def login(browser, phone, pwd):
    browser.get('https://www.ehuixue.cn/index/personal/index.html')
    # time.sleep(5)
    button = EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#nav > div > ul > li.loginstyle > a > span:nth-child(1)'))
    WebDriverWait(browser, 180).until(button)

    button = browser.find_element(By.CSS_SELECTOR, '#nav > div > ul > li.loginstyle > a > span:nth-child(1)')
    button.click()

    WebDriverWait(browser, 180).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#layui-layer-iframe100001"))
    )

    browser.switch_to.frame('layui-layer-iframe100001')

    account_input = browser.find_element(By.ID, 'account1')
    pwd_input = browser.find_element(By.ID, 'pwd')
    account_input.send_keys(phone)
    pwd_input.send_keys(pwd)

    login_btn = browser.find_element(By.CSS_SELECTOR, "body > div > div.login-item > button")
    login_btn.click()

    # get_code_and_confirm(browser)
    browser.switch_to.default_content()
    try:
        element_present = EC.presence_of_element_located((By.NAME, "layui-layer-iframe100001"))
        WebDriverWait(browser, 120).until_not(element_present)
        logging.info("登录成功")
    except TimeoutException:
        logging.error("登录超时，2min内没有成功登录，请检查是否需要手动登录一次")


def get_captcha_code(browser):
    captcha_element = browser.find_element(By.ID, 'verifyimg1')
    captcha_url = captcha_element.get_attribute('src')
    # logging.debug(captcha_url)

    ck = get_ck(browser)
    return get_code(captcha_url, ck)


def get_code(captcha_url, ck):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'accept': '*/*',
        'Cookie': ck
    }
    captcha_data = requests.get(url=captcha_url, headers=headers).content
    # 将验证码图片保存到文件中
    # with open('captcha.png', 'wb') as f:
    #     f.write(captcha_data)
    uname, pwd = get_api_info()
    result = base64_api(uname=uname, pwd=pwd, captcha_data=captcha_data, typeid=1)
    logging.info("识别到验证码为：" + result)
    return result


def get_api_info():
    with open('../../config.yaml', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    api_uname = config['api']['uname']
    api_pwd = config['api']['pwd']
    return api_uname, api_pwd


def get_ck(browser):
    cookies = browser.get_cookies()
    ck = ""
    for ck_dict in cookies:
        name = ck_dict['name']
        value = ck_dict['value']
        ck = ck + str(name) + "=" + str(value) + ";"
    # logging.info(ck)
    return ck


def enter_class(browser, cid):
    time.sleep(3)
    browser.get('https://www.ehuixue.cn/index/study/inclass.html?cid=' + str(cid))


def play(browser):
    play_btn = browser.find_element(By.CSS_SELECTOR,
                                    '#playercontainer > div.jw-controls.jw-reset > div.jw-display-icon-container.jw-background-color.jw-reset > div')
    play_btn.click()

    # 等待3s后再获取时长，防止获取不到
    time.sleep(3)
    video = browser.find_element(By.CSS_SELECTOR, '#playercontainer > div.jw-media.jw-reset > video')
    video_duration = browser.execute_script("return arguments[0].duration", video)
    logging.info("待播放视频时长" + str(video_duration) + "s")

    # （随机）视频任务点，目前只支持随堂练习，和验证码
    try:
        # enter_code(browser, video_duration)
        # finish_work(browser, video_duration)
        task1 = threading.Thread(target=enter_code, args=(browser, video_duration))
        task2 = threading.Thread(target=finish_work, args=(browser, video_duration))
        task1.start()
        task2.start()

    except TimeoutException:
        logging.info("something error")

    # 等待播放下一节视频按钮出现
    try:
        next_btn_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#app > section > main > div.left > div > div.cview > div.studyend > div > button"))
        WebDriverWait(browser, int(video_duration) + 30).until(next_btn_present)

        # 点击播放下一节视频
        time.sleep(2)
        next_btn = browser.find_element(By.CSS_SELECTOR,
                                        "#app > section > main > div.left > div > div.cview > div.studyend > div > button")
        next_btn.click()
        logging.info("视频播放完成")
    except NoSuchElementException:
        logging.info("没有找到下一节按钮，也许已经刷完了")
        # 停止脚本
        browser.quit()
        return

    time.sleep(5)
    logging.info("开始播放下一个视频")
    # 递归，继续往下刷
    play(browser)


def enter_code(browser, video_duration):
    try:
        # 验证码检测
        iframe = EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#layui-layer-iframe100001"))
        WebDriverWait(browser, int(video_duration) + 1).until(iframe)
        logging.info("检测到验证码,开始识别...")
        browser.switch_to.frame('layui-layer-iframe100001')
        get_code_and_confirm(browser)
        browser.switch_to.default_content()

    except TimeoutException:
        logging.info("没有验证码...")


def get_code_and_confirm(browser):
    code = get_captcha_code(browser)
    captcha_input = browser.find_element(By.ID, 'verify')
    time.sleep(1)
    captcha_input.send_keys(code)
    btn = browser.find_element(By.CSS_SELECTOR, 'body > div > div.login-item > button')
    time.sleep(2)
    btn.click()


def finish_work(browser, video_duration):
    try:
        close_btn_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span.layui-layer-setwin > a"))
        WebDriverWait(browser, int(video_duration) + 1).until(close_btn_present)
        # 关闭随堂练习（需要提前完成练习才会有关闭按钮）
        time.sleep(2)
        close_btn = browser.find_element(By.CSS_SELECTOR, "span.layui-layer-setwin > a")
        close_btn.click()
        logging.info("已完成随堂练习")
    except TimeoutException:
        logging.info("没有随堂练习...")


def main(env, phone, pwd, cid):
    if env == "win":
        browser = init_browser_on_window()
    elif env == "centos":
        browser = init_browser_on_centos()
    elif env == "win-no-head":
        browser = init_browser_on_window_with_no_head()
    else:
        logging.error("请选择环境: centos 或 win")
        return
    login(browser, phone, pwd)
    enter_class(browser, cid)
    time.sleep(5)
    play(browser)


def base64_api(uname, pwd, captcha_data, typeid):
    base64_data = base64.b64encode(captcha_data)
    b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]


if __name__ == '__main__':
    # 注意config.yaml 路径
    # 环境类型： win centos win-no-head
    # phone 账号  pwd 密码   cid 需要刷的课程的cid
    # from src.exercises.logUtil import log as logging
    main(env="win", phone="1621*******", pwd="1234", cid=39271)
