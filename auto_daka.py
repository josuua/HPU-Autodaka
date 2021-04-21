import time
import json
import requests
from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def printLog(info_type="", title="", info=""):
    """
    打印日志
    :param info_type: 日志的等级
    :param title: 日志的标题
    :param info: 日志的信息
    :return:
    """
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = now + "  " + info_type + "  " + title + "  " + info
    if info_type == "ERROR":
        print("\033[0;31m" + log + "\033[0m\n")
    elif info_type == "INFO":
        print(log)
    else:
        print(log)
        return
    with open("task.log", "a", encoding="utf-8") as log_a_file_io:
        log_a_file_io.write(log + "\n")


def calc(img_base64: str):
    """
    根据传入的图片计算值并返回
    :param img_base64: 图像数据，base64编码后进行urlencode，需去掉编码头（data:image/jpeg;base64,)
    :return: int: 计算后的数值
    """
    # 请求`access_token`
    oauth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + API_Key + \
                "&client_secret=" + Secret_Key
    token = requests.get(oauth_url).json()['access_token']

    # 通用文字识别 如果你觉得识别错误率比较高，请将下面一行注释掉，将高精度识别的注释打开
    # api_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic" + "?access_token=" + str(token)
    # 高精度识别
    api_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic" + "?access_token=" + str(token)

    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'image': str(img_base64)
    }
    res = requests.post(api_url, headers=header, data=data).json()
    # response like {'words_result': [{'words': '1+5=?'}], 'log_id': 1383448933996429312, 'words_result_num': 1}
    return eval(res['words_result'][0]['words'][0:3])


def task(username, password, name):
    """
    :param name: 学生姓名
    :param username: 学号
    :param password: 密码
    :return:
    """
    try:
        browser.get("https://ehall.hpu.edu.cn/")
        browser.find_element_by_xpath('//*[@id="username"]').clear()
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(str(username))
        browser.find_element_by_xpath('//*[@id="password"]').clear()
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(str(password))
        # 获取验证码

        verify_code = \
            wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="login-form"]/div[2]/div[4]/img'))).get_attribute(
                "src").split(",")[-1].replace("%0A", '\n')
        if verify_code == "":
            time.sleep(5)
            verify_code = \
                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="login-form"]/div[2]/div[4]/img'))).get_attribute(
                    "src").split(",")[-1].replace("%0A", '\n')
        browser.find_element_by_xpath('//*[@id="captcha"]').clear()
        browser.find_element_by_xpath('//*[@id="captcha"]').send_keys(str(calc(verify_code)))
        browser.find_element_by_xpath('//*[@id="login-submit"]').click()
        # 访问页面
        browser.get("https://ehall.hpu.edu.cn/infoplus/form/XSMRJKSB/start")
        # 判断是否登录成功
        # TODO：在这可以补充填写详细信息的代码
        # 这里就直接提交了，如果你原来提交过的话，会有缓存的
        # 等待异步加载
        # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="btn_group"]/li[1]'))).click()
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, '提交'))).click()
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[contains(@class, "dialog_button") and contains(@class, "default")]'))).click()
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[contains(@class, "dialog_button") and contains(@class, "default")]'))).click()
        if SCREENSHOT:
            time.sleep(1)
            browser.save_screenshot(
                './screenshot/' + str(username) + time.strftime("%m_%d_%H_%M_%S", time.localtime()) + ".png")
        # 输出日志
        printLog("INFO", str(username) + str(name) + "提交成功")
        # 注销
        browser.get("https://ehall.hpu.edu.cn/taskcenter/logout")
        return True

    except Exception as e:
        error.append([username, password, name])
        # 输出日志
        printLog("ERROR", str(username) + "提交错误, 稍后重做", str(name) + str(e.__dict__))
        browser.get("https://ehall.hpu.edu.cn/taskcenter/logout")
        return False


if __name__ == '__main__':
    # 是否完成后截图
    SCREENSHOT = False
    # 是否一直重复错误项：(不建议开启)
    ANY_ERROR = False

    # 获取API_Key、Secret_Key、用户信息
    with open('config.json', "r") as f:
        CONFIG = json.load(f)
        API_Key = CONFIG['API_Key']
        Secret_Key = CONFIG['Secret_Key']
        users = CONFIG['userInfo']

    chrome_options = webdriver.ChromeOptions()

    # 无头模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1920,1050")

    # 如果你是其它的系统请修改下面一行
    # mac like this：
    browser = webdriver.Chrome(executable_path="drivers/chromedriver", options=chrome_options)
    # windows like this：
    # browser = webdriver.Chrome(executable_path="drivers/chromedriver.exe", options=chrome_options)

    # 设置等待时间
    wait = WebDriverWait(browser, 10)
    error = []
    # 依次完成任务
    for user in users:
        task(username=user['id'], password=user['pw'], name=user.get("name", "未知"))
    # 重复错误的
    printLog("INFO", "错误重做")
    # 一直重复
    if ANY_ERROR:
        for _ in error:
            task(_[0], _[1], _[2])
    else:
        l = len(error)
        for _ in range(l):
            task(error[_][0], error[_][1], error[_][2])

    printLog("INFO", "执行完毕")
    browser.close()
