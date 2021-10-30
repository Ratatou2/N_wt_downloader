from selenium import webdriver
import time

driver = webdriver.Chrome("chromedriver.exe")
driver.get('https://comic.naver.com/webtoon/detail?titleId=650305&no=335&weekday=sat')
time.sleep(3)

web_elements = driver.find_elements_by_class_name('wt_viewer')
# test = driver.find_elements_by_css_selector('#comic_view_area > div.wt_viewer')
# test2 = driver.find_elements_by_xpath('//*[@id="comic_view_area"]/div[1]')

img_list = []
for link in web_elements:
    trans_texts = link.get_attribute('innerHTML').strip()
    img_list.append(trans_texts)
print(trans_texts)
raw_link = img_list[0].split('comic content')

for link in raw_link:
    if 'img src' in link:
        left = link.find('img src')
        right = link.find(' title')
        print(link[left+8:right])
