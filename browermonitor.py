#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from Monitor import *

monitor = Monitor()
#print(dir(monitor))
monitor.Start()
monitor.genNewRecord()
# print(dir(monitor.proxy))
#13000000000 存在
# monitor.driver.get("http://member.ehaier.com/toRegister.html")
# monitor.driver.get("https://sso.unipus.cn/sso/findPw.html")
monitor.driver.get("https://segmentfault.com/user/forgot")
# monitor.driver.get("http://www.cndns.com/members/register.aspx")
monitor.getPhoneApi()

# monitor.driver.get("https://s.taobao.com/search?q=薯条")
# targetUrl = "https://s.taobao.com/api.*?"
# text = monitor.getContentText(targetUrl)

# tycmonitor.Quit()