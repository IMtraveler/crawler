# -*- coding: utf-8 -*- 
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import csv
import sys

#開啟瀏覽器，進入有很多景點的主頁面--------------------
def open_main_browser():
	binary = FirefoxBinary("C:\Program Files (x86)\Mozilla Firefox\\firefox.exe")
	browser = webdriver.Firefox(firefox_binary = binary)
	url = "https://www.tripadvisor.com.tw/Attractions-g1432365-Activities-Xinbei.html"
	print(url)
	browser.get(url)
	return browser

def func_sal(browser):
	see_all_link = browser.find_elements_by_class_name("see_all_link")
	print("see_all_link:" + str(len(see_all_link)))
	return see_all_link

def get_name_and_address(browser):
	tag = re.compile('</?\w+[^>]*>')
	j=0
	time.sleep(3)   #避免他網頁還沒跑完就要抓資料而失敗
	soup = BeautifulSoup(browser.page_source, "html.parser")
	
	heading = soup.select("#HEADING")
	notag_head = re.sub(tag,'',str(heading))
#	str_head = "".join(notag_head.split())
	if soup.select(".altHead"):
		altHead = soup.select(".altHead")[0].text
		print(altHead)
		Chinese_title = re.sub(altHead,'',str(notag_head))
		str_head = "".join(Chinese_title.split())
		print(str_head)
	else:
		str_head = "".join(notag_head.split())
		altHead = "NULL"
	address = soup.select(".detail_section.address")
	str_adrs = re.sub(tag,'',str(address))
	#print(type(str_head.encode('utf-8')))

	class_tag = soup.select(".header_detail.attraction_details")  #list
	class_tag = re.sub(tag or ', ','+',str(class_tag[0].text.strip()))
	print(class_tag)

	str_head_decode = str(str_head.encode('utf-8').decode('utf-8',"ignore")).strip("][")
	altHead_decode = str(altHead.encode('utf-8').decode('utf-8',"ignore")).strip("][")
	str_adrs_decode = str(str_adrs.encode('utf-8').decode('utf-8',"ignore")).strip("][")

	try:
		print("景點 str_head_decode:" + str_head_decode)
		print("地址 str_adrs_decode:" + str_adrs_decode)
		print("------------------------")
		context = [str_head_decode, altHead_decode ,str_adrs_decode, class_tag]
		w.writerows([context])
	except:
		print("NOOOOOOOOOOOO")

#-------------------------------------------
browser = open_main_browser()
soup = BeautifulSoup(browser.page_source, "html.parser")

mainWindow = browser.current_window_handle   #最大主頁

#開啟csv檔----------------------------------------
headers = ['chinese_name', 'english_name', 'address', 'class_tag']
f = open("new_tpe_sight.csv",  "w", newline='')
w = csv.writer(f)
w.writerows([headers])

#依次點選多個類別，以獲取更多的景點，維持在次主頁面------
see_all_link = func_sal(browser)
k=1
total_sight_count = 0
for x in range(0,len(see_all_link)-1):
	see_all_link = func_sal(browser)
	see_all_link[k].click()
	print( "這是see_all_link 第 "+ str(k))

	second_main_Window = browser.current_window_handle  #次主頁面
	url = browser.current_url
	browser.get(url)
	print("Switch_to_次主頁面")

	next = browser.find_elements_by_class_name("nav.next")  #看有沒有next
	page_count = 0      #第幾頁
	next_count = len(next)  #有幾頁
	sight_count = 0     #一個類別總共有多少個景點(包含換頁的)
	if len(next)!=0:
		print("有next，next_count: " + str(next_count))
		print("type of next: " + str(type(next)))

	while page_count < len(next)+1:  #有下一頁，且還沒看完
		i=0
		title = browser.find_elements_by_class_name("display_text.ui_button.original")   #抓景點
		print("這頁有幾個景點: "+str(len(title)))
		times = len(title)

		#依次點選多個景點，維持在主頁面---------------------
		while i < times:
			title[i].click()
			i = i+1
			sight_count = sight_count + 1
			print(sight_count)
			browser.switch_to_window(second_main_Window)
		if next_count != 0:			#換頁之後要再做處理才可以用back
			next[page_count].click()
			next_count = next_count -1
		page_count = page_count + 1

		j=0
		print("開始關頁囉!!!!!yeeeeeeeeeeeee")
		while j < times:
			print(j)
			browser.switch_to_window(browser.window_handles[1])
			get_name_and_address(browser)
			total_sight_count += 1
			browser.close()
			j = j+1
			print(total_sight_count)
		browser.switch_to_window(browser.window_handles[0])

	#browser.switch_to_window(browser.window_handles[0])
	for back_times in range(0,len(next)+1):   #從0開始 < 第二個參數
		print("hello")
		browser.back()
	print("BACK to mainWindow")
	k = k +1
	#browser.close()

f.close()

"""Google GeoAPI 金鑰:
AIzaSyDUXjdEFQXQ9j59FWlRHZTlaAfyj2Qiuu0

https://maps.googleapis.com/maps/api/geocode/json?address=040-0001&key=AIzaSyDUXjdEFQXQ9j59FWlRHZTlaAfyj2Qiuu0

"""

#在Windows執行的話要在cmd輸入: chcp 65001   (從cp950編碼轉換為UTF-8)