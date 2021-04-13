#! /usr/bin/python3.6
# coding:utf-8
import time
from time import sleep
from aip import AipOcr
from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json


def auoto_daka(username, password):
    print("-------------------------------------")
    print("用户 %s 开始打卡！" % username)
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    str1 = '执行时间： ' + t + '\n'
    print(str1)

    # 进入chrome的无头模式，方便部署服务器上使用
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get("https://ehall.hpu.edu.cn/infoplus/form/XSMRJKSB/start")  # 进入打卡界面，需要登陆理工大统一认证平台
    sleep(1)
    browser.save_screenshot('./save_screenshot.png')  # 截取理工大统一认证平台界面，方便后面得到验证码

    # 输入账号和密码
    browser.find_element_by_id("username").send_keys(username)  
    browser.find_element_by_id("password").send_keys(password)  
    print("账号密码输入成功！")
    # 截取验证码
    captcha_image = browser.find_element_by_xpath('//*[@id="login-form"]/div[2]/div[4]/img')
    left = captcha_image.location['x']
    top = captcha_image.location['y']
    right = left + captcha_image.size['width']
    bottom = top + captcha_image.size['height']
    image = Image.open('./save_screenshot.png')
    code_image = image.crop((left, top, right, bottom))
    code_image.save('./code_image.png')
    '''这里写了两个截取验证码的方法，是因为在测试和部署到服务器后，验证码的位置可能不太一样，
       上面是部署在服务器上的截取方法，下面是测试时候的截取方法
    left = 2 * captcha_image.location['x']
    top = 2 * captcha_image.location['y']
    right = left + 2 * captcha_image.size['width'] - 10
    bottom = top + 2 * captcha_image.size['height'] - 10
    image = Image.open('./save_screenshot.png')
    code_image=image.crop((left,top,right,bottom))
    code_image.save('./code_image.png')
    '''
    print("验证码截取成功！")
    # 调取百度文字识别的API，对截取的图片进行识别，并将计算结果输入进去
    APP_ID = '23968112'
    API_KEY = 'PBapGk7OGKjepiiuW7I0DBXr'
    SECRET_KEY = 'trI8UrKifcoh61j3b6tkhrQ330YzXiWG'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    i = open('./code_image.png', 'rb')
    img = i.read()
    message = client.basicAccurate(img)
    text = message.get('words_result')
    #print(text)
    print(text[0].get('words'))
    text1 = str(text[0].get('words'))
    captcha_result = int(text1[0]) + int(text1[2])
    browser.find_element_by_id("captcha").send_keys(captcha_result)
    sleep(3)
    browser.find_element_by_id("login-submit").send_keys(Keys.ENTER)
    sleep(2)
    print("跳转成功")
    browser.maximize_window()

    sleep(5)  # 等待内容加载时间

    browser.find_element_by_link_text("提交").click()
    sleep(3:wq
    )
    print("点击提交按钮，等待弹窗出现...")

    browser.find_element_by_class_name("dialog_button.default.fr").click()
    sleep(3)
    browser.find_element_by_class_name("dialog_button.default.fr").click()  # 奈何理工大提交弹窗太多了
    sleep(6)
    browser.quit()
    print("用户 %s 打卡完毕！" % username)
    print("-------------------------------------")
    sleep(10)


if __name__ == '__main__':
    with open('user_info.json', 'r') as f:
        list1 = []
        list2 = []
        data = json.load(f)
        for key, value in data.items():
            list1.append(key)
            list2.append(value)
    for i in range(len(list1)):
        auoto_daka(list1[i], list2[i])
