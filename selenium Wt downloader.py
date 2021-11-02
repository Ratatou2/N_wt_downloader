import time, os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs


def make_wt_url(wt_id):
    basic = 'https://comic.naver.com/webtoon/list?titleId='
    return basic + wt_id


def image_down(URL, count):
    fake_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

    ep_html = requests.get(URL, headers=fake_header)
    with open(str(count).zfill(3) + '.png', 'wb+') as f:
        f.write(ep_html.content)


def downloads_imgs(temp_text):
    img_links = temp_text.split(' false" src="')

    count = 0
    for link in img_links:
        if 'https://image-comic.pstatic.net/webtoon/' in link:
            left = link.find('https://image-comic.pstatic.net/webtoon/')
            right = link.rfind('.jpg')

            refine_link = link[left:right+4]
            print(refine_link)
            image_down(refine_link, count)
            count += 1


def set_directory():
    directory = 'D:/'
    ask_input = input('기본 디렉토리를 변경하시겠습니까? (y/n) : ')

    if ask_input == 'y':
        temp = input('지정할 디렉토리를 입력해주세요 : ')
        directory = temp + '/'
    elif ask_input == 'n':
        print('기본 디렉토리를 변경하지 않습니다\n')

    try:
        os.chdir(directory)
    except:
        print('[Warning]')
        print(f'경로 [ {directory} ]가 확인되지 않습니다.')
        print(f'[ C:/ ]로 경로를 변경합니다')
        directory = 'C:/'

    return directory


if __name__ == '__main__':
    driver_dir = os.getcwd()
    fake_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    # wt_id = input('웹툰의 ID를 입력해주십시오 : ')
    wt_id = '729563'
    title_url = make_wt_url(wt_id)
    html = requests.get(title_url, headers=fake_header)
    soup = bs(html.text, 'html.parser')

    ep_info_all = soup.select_one('#content > div.comicinfo > div.detail > h2')

    pres_dir = set_directory()

    wt_info = [t.text.strip() for t in ep_info_all]
    wt_title = wt_info[0]
    print(wt_title)

    try:
        os.mkdir(pres_dir + wt_title)
    except FileExistsError:
        print('같은 이름의 디렉토리가 이미 있는 것 같습니다')
        os.mkdir(pres_dir + wt_title)

    driver = webdriver.Chrome(driver_dir + '/' + 'chromedriver.exe')

    time.sleep(30)

    s = requests.session()

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    s.headers.update(headers)
    driver.get_cookies()

    for cookie in driver.get_cookies():
        c = {cookie['name'] : cookie['value']}
        s.cookies.update(c)

    wt_basic_url = 'https://comic.naver.com/webtoon/detail?titleId=' + wt_id + '&no='
    rem_ep_title = str()
    for i in range(1, 1000):

        print(wt_basic_url + str(i))
        response = s.get(wt_basic_url + str(i))

        web_elements = driver.find_elements_by_class_name('wt_viewer')

        img_list = []
        for link in web_elements:
            trans_texts = link.get_attribute('innerHTML').strip()
            img_list.append(trans_texts)

        soup = bs(response.text, 'html.parser')

        raw_links = []
        for pars in soup:
            raw_links.append(pars)

        make_file = open(driver_dir + '/' + 'temp1.txt', 'w', encoding='UTF-8')  # [1] 참고
        print(raw_links, file=make_file)
        make_file.close()


        temp_file = open(driver_dir + '/' + 'temp1.txt', 'r', encoding='UTF-8')
        temp_text = temp_file.read()

        refine_title = str()
        find_wt_title = temp_text.split('meta')
        for link in find_wt_title:

            if 'property="og:description' in link:
                left = link.find('nt="')
                right = link.rfind('" property="og:description"/>')
                refine_title = link[left+4:right]
                print(refine_title)

            if rem_ep_title == refine_title:
                break


        ep_dir_title = '[' + str(i).zfill(3) + '] ' + refine_title
        os.chdir(pres_dir + wt_title)
        os.mkdir(ep_dir_title)
        print(f'현재 [{str(i).zfill(3)}] {refine_title} 작업 중입니다')
        os.chdir(pres_dir + wt_title + '/' + ep_dir_title)

        downloads_imgs(temp_text)

        os.chdir('..')

        rem_ep_title = refine_title




'''
[1] cp949' codec can't encode character '\xa0' in position 3379: illegal multibyte sequence 해결 방법 UTF 추가
'''