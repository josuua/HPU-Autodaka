# 声明：编写此脚本的目的是为了研究百度云、python等技术，不要进行非法使用。为了大家的健康，请大家按照实际情况填写。
# 正在不断的优化，请大家稍安勿躁。有任何问题请发送至receive_problem@163.com<br>
# 感谢一位网友的支持，他写的会更详细一些，具体链接如下<a>https://github.com/FionJones/HPU-Autodaka</a>
* 如果有的学生实在不想部署整个环境的话可以把登陆河南理工大学统一身份认证的<b>学号</b>和<b>密码</b>发送邮箱，会一一进行回执。
# 前言
如果你现在使用自动打卡的话，说明我已经就是你的学长了，起初是为了女朋友的方便，但是为了回馈母校的学弟和学妹们，就随便写了个脚本，如有问题请在Issues提出问题，并留下自己的联系方式，我会主动联系。
# 使用方法
1. 购买百度云服务器，有学生优惠，三个月18块钱。（https://cloud.baidu.com/campaign/campus-2018/index.html?unifrom=eventpage）<br>
2. 注册文字识别API，选择通用文字（高精度版本），切记是高精度版本，因为代码里调用的是高精度版本，这个一天可以免费检测500次，绝对够用。（https://cloud.baidu.com/product/ocr_general）<br>
3. 服务器的使用方法不在多说，网上一大堆。但是需要安装pip3，git，chrome，chromedriver，selenium，pillow，baidu-aip等环境<br>
4. 将文件git到服务器上，然后将代码中的账号和密码改为自己的，代码中的APP_ID，API_KEY，SECRET_KEY改为自己注册的信息，然后配置自动执行文件
# 更新
可以加周围同学的学号，格式已经放到user_info.json文件中。



---

#### 怎么使用？

1.  安装`Python 3`环境

    1.  <[Python Mirror (taobao.org)](https://npm.taobao.org/mirrors/python/3.9.0/)>访问这个页面，下载符合你系统的版

2.  下载这个项目

    `git clone  https://github.com/cilicilis/HPU-Autodaka.git`

    如果你没有`Git`的话可以直接访问<https://github.com/cilicilis/HPU-Autodaka.git>下载`zip`

3.  安装依赖的包

    1.  首先进入文件夹

        在终端前往`HPU-Autodaka/`，`windows`的同学可以在`HPU-Autodaka`文件夹下按住`shift+鼠标右键`打开`powershell`

    2.  运行`pip install -r requirements.txt`

4.  申请百度`OCR`接口

    1.  访问<[文字识别_通用场景文字识别-百度AI开放平台 (baidu.com)](https://cloud.baidu.com/product/ocr_general)>

    2.  访问`控制台->文字识别->应用列表->创建应用`

    3.  创建成功后复制你的`API_Key`,`Secret_Key`到`config.json`相应位置

        注意：**泄露你的`API_Key`,`Secret_Key`可能会导致你的识别额度超标**

5.  配置`config.json`

    ```json
    {
      "API_Key": "在这里输入获取的API_Key",
      "Secret_Key": "在这里输入获取的Secret_Key",
      "userInfo": [
        {
          "id": "311000000001",
          "pw": "054321"
        },{ # 你可以添加多个同学，如果不需要的话请删除
          "id": "311000000002",
          "pw": "012345"
        }
      ]
    }
    ```

6.  安装浏览器以及浏览器驱动

    1.  如果你没有`Chrome`浏览器请访问<[Google Chrome 网络浏览器](https://www.google.com/chrome/)>下载浏览器
    2.  浏览器驱动位于`./drivers/`下，如果浏览器驱动于你的浏览器不兼容请参考：
        -   Chrome
            -   首先访问`chrome://version/`查看浏览器的版本
            -   去访问http://chromedriver.storage.googleapis.com/index.html下载对应的`webdriver`放到`drivers`下
        -   Edge
            -   访问`edge://version/`查看浏览器的版本
            -   https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/下载对应的`webdriver`放到`drivers`下
        -   Firefox
            -   访问`about:version`查看浏览器的版本
            -   https://github.com/mozilla/geckodriver/releases/下载对应的`webdriver`放到`drivers`下

7.  运行`python auto_daka.py`,默认会保存截图到`./screenshot/`下，你可以将`auto_daka.py`的`SCREENSHOT = True`改为`SCREENSHOT = False`



### 免责声明

>   这个脚本只是方便健康的同学打卡的工具，如果你健康状况异常(包括但不限于发烧、干咳、胸闷、乏力、腹泻)的，请及时报告老师，并**立刻停止运行该脚本**。
>
>   **你一旦运行这个脚本，即你同意所有内容，请仔细阅读**。由于你没有及时上报真实的健康状况而**导致的所有后果**，由你**本人承担**。



### 问题

1.  为什么我无法运行

    >   请检查你是否将`python`加入环境变量

    

2.  为什么窗口一闪而过

    >   你可以通过 终端/命令提示符/powershell 来运行，截图报错信息，提交`issue`



