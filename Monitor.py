#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
"""step 1 导入依赖库"""
from os import path
from browsermobproxy import Server
from selenium import webdriver
import re
import pdb
import func as zfuncs
from selenium.webdriver.common.keys import Keys
import time, sys, string, random, json, requests

"""step 2 新建浏览器监控类"""
class Monitor(object):
    """
    step 3 配置chromedriver 和 browermobproxy 路径
    需要使用完整路径，否则browsermobproxy无法启动服务
    我是将这两个部分放到了和monitor.py同一目录
    同时设置chrome为屏蔽图片，若需要抓取图片可自行修改
    """
    PROXY_PATH = path.abspath("F:/rudder/py/accountApi/utils/browsermob-proxy-2.1.1/bin/browsermob-proxy.bat")
    CHROME_PATH = path.abspath("F:/rudder/py/accountApi/utils/chromedriver")
    CHROME_OPTIONS = {"profile.managed_default_content_settings.images":2}
    canFoundInText = False

    def __init__(self):
        """
        类初始化函数暂不做操作
        """
        pass
        
    def initProxy(self):
        """
        step 4 初始化 browermobproxy
        设置需要屏蔽的网络连接，此处屏蔽了css，和图片（有时chrome的设置会失效），可加快网页加载速度
        新建proxy代理地址
        """
        self.server = Server(self.PROXY_PATH)
        self.server.start()        
        self.proxy = self.server.create_proxy()
        self.proxy.blacklist(["http://.*/.*.css.*","http://.*/.*.jpg.*","http://.*/.*.png.*","http://.*/.*.gif.*"],200)
        
    def initChrome(self):
        """
        step 5 初始化selenium， chrome设置
        将chrome的代理设置为browermobproxy新建的代理地址
        """            
        chromeSettings = webdriver.ChromeOptions()
        chromeSettings.add_argument('--proxy-server={host}:{port}'.format(host = "localhost", port = self.proxy.port))
        chromeSettings.add_experimental_option("prefs", self.CHROME_OPTIONS)
        self.driver = webdriver.Chrome(executable_path = self.CHROME_PATH, chrome_options = chromeSettings)
     
    def genNewRecord(self, name = "monitor", options={'captureContent':True}):
        """
        step 6 新建监控记录，设置内容监控为True
        """
        self.proxy.new_har(name,options = options)
    
    def getContentText(self, targetUrl):
        """
        step 7 简单的获取目标数据的函数
        其中 targetUrl 为浏览器获取对应数据调用的url，需要用正则表达式表示
        """
        if self.proxy.har['log']['entries']:
            for loop_record in self.proxy.har['log']['entries']:
                try:
                    print(loop_record)
                    # if re.fullmatch(targetUrl , loop_record["request"]['url']):
                        # return loop_record["response"]['content']["text"]
                except Exception as err:
                    print(err)
                    continue
        return None

    
    def Start(self):
        """step 8 配置monitor的启动顺序"""
        try:
            self.initProxy()
            self.initChrome()
        except Exception as err:
            print(err)
    
    def Quit(self):
        """
        step 9 配置monitor的退出顺序
        代理sever的退出可能失败，目前是手动关闭，若谁能提供解决方法，将不胜感激
        """
        self.driver.close()
        self.driver.quit()
        try:
            self.proxy.close()
            self.server.process.terminate()
            self.server.process.wait()
            self.server.process.kill()
        except OSError:
            pass

    def getPageContent(self):
        print(666)






    #获取手机号是否存在接口, 返回-1未查找到用户名输入框，返回-2填写后无HTTP请求，返回-3填写测试数据后未发现请求包，返回-4无法抓取已注册请求包（现有测试数据都未注册）
    def getPhoneApi(self):
        if self.server == None: 
            return False
        # self.driver.get('http://www.cndns.com/members/register.aspx')
        element = zfuncs.z_get_input_element_by_key_phone(self.driver)#获取手机号码输入框
        if element==False:
            print "未查找到手机号码输入框"
            return -1
        req_url = self.get_phone_api_url(element)#获取请求URL，用于定位请求包
        # print req_url
        if req_url==False:
            element = zfuncs.z_get_input_element_by_key_submit(self.driver)#提交
            req_url = self.get_click(element)#获取请求URL，用于定位请求包
            if req_url==False:
                print "未发现请求包"
            #return -2
        # print(entry['request']['url'].find(req_url))
        #使用常用用户名测试，获取用户存在响应包
        # for line in open("./keys/phone.value"):
            # line = line.strip('\n')
            # entry = self.find_entry_by_string(element, line)
        #     if entry!=False and entry['request']['url'].find(req_url)!=-1:#确认请求包
                #判断是否已注册请求包
        line = "1300000"
        if self.canFoundInText == False:
            is_exist = zfuncs.z_get_isexists_by_key_exists(self.driver)
        else:
            is_exist = zfuncs.z_get_element_by_key_exists(self.driver)
        if is_exist!=False:
            print line+"：发现已注册"
            # return entry #返回当前请求包
        else:
            print line+"：未发现已注册"
        #     else:
        #         print line+"：未发现请求包"
        #         return -3
            
        # return -4

    #获取手机号是否存在接口的请求URL
    def get_phone_api_url(self, element):
        if self.server == None: 
            return False
        str = '1300'+self.id_generator(7, '0123456789')#生成测试手机号
        str = '13000000000' ########################### guding
        entry = self.find_entry_by_string(element, str)
        
        if entry==False:
            print("输入后未发起请求")
            return False
        
        url = entry['request']['url']
        return url.split("?")[0]

        #定位请求包位置, element为用来填写内容的input输入框
    def find_entry_by_string(self, element, keystr):
        #获取输入内容后的所有网络请求
        entries = self.get_entries(element, keystr)
        # pdb.set_trace() 
        # print("请求后返回"+dir(entries))
        #查找是否有网络请求
        entry = self.find_har_by_string(entries, keystr)
        if entry==False:
            print "未发起网络请求"
            return False
        print "发现填写后会发起网络请求"
        
        return entry
    
    #获取输入内容后的所有网络请求
    def get_entries(self, element, keystr):
        if element==False:#该页未查找到输入用户名的地方
            return False
        if element.get_attribute('name')!='':
            print "Input name: "+element.get_attribute('name')
        if element.get_attribute('id')!='':
            print "Input id: "+element.get_attribute('id')
        print "填写测试字符串："+keystr
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(keystr)
        element.send_keys(Keys.TAB)
        time.sleep(2)#等待请求结束，页面改变
        # print("请求地址"+self.proxy.har['log']['entries'])
        return self.proxy.har['log']['entries']
        
    #查找数组中包含关键字的数组项
    def find_har_by_string(self, arr, keystr):
        if type(arr)!=list:
            print("feilist")
            return False
            #倒序遍历数组，查找关键字符串
        for i in range(0, arr.__len__())[::-1]:
            # print arr[i]
            if json.dumps(arr[i]).find(keystr)!=-1:
                return arr[i]
        return False
            
    #获取随机值
    def id_generator(self, size=6, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    #触发点击事件
    def get_click(self, element):
        if element==False:
            return False
        
        element.click()
        print("触发点击事件")
        time.sleep(2)#等待请求结束，页面改变
        # print("请求地址"+self.proxy.har['log']['entries'])
        return self.proxy.har['log']['entries']