#coding:utf-8
from selenium.webdriver.common.keys import Keys
import time, sys, string, random, json, requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#获取手机的input对象，如果失败返回False
def z_get_input_element_by_key_phone(driver):
	input_boxes = driver.find_elements_by_xpath("//input[@type='text']")
	for line in open("./keys/phone.key"):
		line = line.strip('\n')
		#print("0-0".line)
		for element in input_boxes:#先查找name
			if element.get_attribute('name').find(line) != -1 and element.is_displayed(): #需要判断输入框用户是否可见
				print("-1-")
				return element
		for element in input_boxes:#查找id
			if element.get_attribute('id').find(line) != -1 and element.is_displayed(): 
				print element.get_attribute('id')
				print("-2-")
				return element
	return False

def z_get_input_element_by_key_submit(driver):
	input_boxes = driver.find_elements_by_xpath("//input")
	for element in input_boxes:#先查找name
		if element.get_attribute('type').find("submit") != -1 and element.is_displayed(): #需要判断输入框用户是否可见
			print("-1-")
			return element
	for element in input_boxes:#查找id
		if element.get_attribute('id').find("submit") != -1 and element.is_displayed(): 
			print element.get_attribute('id')
			print("-2-")
			return element
	return False

#获取用来判断是否已注册字符串的对象，遍历标签，速度慢
def z_get_element_by_key_exists(driver):
	eles = driver.find_elements(By.XPATH, '//a | //span | //li | //b | //font | //div')
	print(eles)
	#eles = driver.find_elements(By.XPATH, '//span')
	for line in open("./keys/exists.key"):
		line = line.strip('\n')
		for ele in eles:
			if ele.get_attribute("innerHTML").find('<')!=-1 or ele.get_attribute("innerHTML")=='':#如果包含html标签则无视掉
				continue
			else:
				#print ele.get_attribute("outerHTML")
				if(ele.get_attribute("innerHTML").find(line)!=-1):
					return ele
	return False

#获取用来判断是否已注册字符串，直接搜索文本，速度快，准确性低
def z_get_isexists_by_key_exists(driver):
	# print driver.find_element(By.XPATH, '//body').get_attribute("innerHTML")
	# bodyhtml = driver.find_element(By.XPATH, '//body').get_attribute("innerHTML")
	#print driver.find_element_by_xpath('//body').get_attribute("innerHTML")
	bodyhtml = driver.find_element_by_xpath('//body').get_attribute("innerHTML")
	# print(bodyhtml)

	file_object = open('log.txt', 'w')
	file_object.write(bodyhtml)
	file_object.close( )

	# print "0--0".bodyhtml1
	for line in open("./keys/exists.key"):
		line = line.strip('\n')
		if(bodyhtml.find(line)!=-1):
			print line
			return 'Found'
	return False

