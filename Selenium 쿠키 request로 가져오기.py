# 참고 : https://m.blog.naver.com/draco6/221664143794

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Chrome('chromedriver.exe')

time.sleep(30)
s = requests.session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
s.headers.update(headers)
driver.get_cookies()

for cookie in driver.get_cookies():
    c = {cookie['name'] : cookie['value']}
    s.cookies.update(c)

response = s.get('https://comic.naver.com/webtoon/detail?titleId=729563&no=114&weekday=sat')
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)