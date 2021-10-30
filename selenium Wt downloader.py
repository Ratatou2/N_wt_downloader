from selenium import webdriver
import requests
import time


def one_pack():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('disable-gpu')
    options.add_argument('window-size=900x1080')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument("lang=ko_KR")

    # 실제브라우져와 동일하게 작동하는 세션루틴실행
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 지정경로에 세션정보를 디스크에 저장하고 실행시마다 재사용함
    options.add_argument('--user-data-dir=D:\program')

    driver = webdriver.Chrome('chromedriver.exe', options=options)

    rec_session = login(driver)

    url = 'https://comic.naver.com/webtoon/detail?titleId=729563&no=114&weekday=sat'
    image_down(make_ep_links(url))


def login(driver):
    # 웹 자원 로드를 위해 암묵적으로 딜레이
    delay_time = 3
    driver.implicitly_wait(delay_time)

    # URL 접근
    driver.get('https://nid.naver.com/nidlogin.login')

    # ID, PW 입력
    id = "jo__oh18"
    pw = "xkfcnfapdlxm0919"
    driver.find_element_by_name('id').send_keys(id)
    driver.find_element_by_name('pw').send_keys(pw)

    # 로그인 버튼 클릭
    driver.find_element_by_xpath('//*[@id="log.login"]').click()
    time.sleep(20)

    return driver


def make_ep_links(ep_URL):
    driver = webdriver.Chrome("chromedriver.exe")

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

    driver.close()
    return cook_link


def image_down(URLS):
    fake_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    count = 0
    for i in URLS:
        ep_html = requests.get(i, headers=fake_header)
        with open(str(count) + '.png', 'wb+') as f:
            f.write(ep_html.content)

        count += 1

if __name__ == '__main__':
    one_pack()