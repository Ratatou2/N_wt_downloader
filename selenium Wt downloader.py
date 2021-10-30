from selenium import webdriver
import requests
import time

fake_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

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

cook_link = []
for link in raw_link:
    if 'img src' in link:
        # 웹 링크로 이미지를 다운로드할 때 양쪽에 "(따옴표)는 빼줘야 함
        left = link.find('img src')
        right = link.find(' title')
        cook_link.append(link[left+9:right-1])

count = 0
for i in cook_link:
    ep_html = requests.get(i, headers=fake_header)
    with open(str(count) + '.png', 'wb+') as f:
        f.write(ep_html.content)

    count += 1