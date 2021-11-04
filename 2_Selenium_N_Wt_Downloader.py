import time, os, requests, shutil, sys
from selenium import webdriver
from bs4 import BeautifulSoup as bs


def my_info():
    print('------------------------------------------------------')
    print('제작자 : Ratatou2')
    print('문의 및 개선 사항은 ws4232@naver.com 으로 메일 부탁드립니다')
    print('https://github.com/Ratatou2')
    print('https://blog.naver.com/ws4232')
    print('------------------------------------------------------')


def end_program():
    while True:
        print()
        a = input("<system> 프로그램을 종료하셔도 됩니다.")
        if a == "q":
            sys.exit()
        else:
            print("<system> 입력받은 문자 : " + a)


def get_end_time(re_time, i):
    print('------------------------------------------------------')
    print('<system> 다운로드가 완료되었습니다')
    end_time = time.time() - re_time
    print(f'<system> 소요된 시간은 {round(end_time)}초 (대략 {round((end_time/60), 1)}분) 입니다')
    print(f'<system> 1분당 [{round(i/round((end_time/60), 2), 1)}편]을 받았습니다')
    print('------------------------------------------------------')
    end_program()


def set_wt_area():
    print('<system> 받고 싶은 회차를 다음 예시와 같이 입력해주세요')
    print(' ex) 7화 한개만 받고 싶은 경우       -> "7~7"  을 입력')
    print(' ex) 2화부터 30화까지 받고 싶은 경우 -> "2~30"  을 입력')
    print(' ex) 50화부터 끝까지 받고 싶은 경우  -> "50~1000" 을 입력')
    print(' ex) 별도의 지정없이 전 회차 다운 받고 싶은 경우 -> 그냥 엔터')
    print('------------------------------------------------------')

    try:
        start_ep, end_ep = map(int, input().split('~'))
    except ValueError:
        start_ep, end_ep = 1, 1000

    return start_ep, end_ep


def clear_text(word):
    special_char = '\/:*?"<>|'
    return ''.join(char for char in word if char not in special_char)


def image_down(URL, count, fake_header):
    ep_html = requests.get(URL, headers=fake_header)
    with open(str(count).zfill(3) + '.png', 'wb+') as f:
        f.write(ep_html.content)


def downloads_imgs(temp_text, fake_header):
    img_links = temp_text.split(' false" src="')

    count = 0
    for link in img_links:
        if 'https://image-comic.pstatic.net/webtoon/' in link:
            left = link.find('https://image-comic.pstatic.net/webtoon/')
            right = link.rfind('.jpg')

            refine_link = link[left:right+4]
            image_down(refine_link, count, fake_header)
            print(f'    <system> {count} 번째 사진 작업중', end='\r', flush=True)
            count += 1


def set_directory():
    directory = 'D:/'
    ask_input = input('<system> 기본 디렉토리를 변경하시겠습니까? (y/n) : ')

    if ask_input == 'y':
        temp = input('<system> 지정할 디렉토리를 입력해주세요 : ')
        directory = temp + '/'
    elif ask_input == 'n':
        print('<system> 기본 디렉토리를 변경하지 않습니다')

    try:
        os.chdir(directory)
    except:
        print('[Warning]')
        print(f'<system> 경로 [ {directory} ]가 확인되지 않습니다.')
        print(f'<system> [ C:/ ]로 경로를 변경합니다')
        print('------------------------------------------------------')
        directory = 'C:/'

    return directory


def get_wt_title(wt_id, fake_header):
    basic = 'https://comic.naver.com/webtoon/list?titleId='

    title_url = basic + wt_id
    html = requests.get(title_url, headers=fake_header)
    soup = bs(html.text, 'html.parser')

    ep_info_all = soup.select_one('#content > div.comicinfo > div.detail > h2')
    pres_dir = set_directory()

    wt_info = [t.text.strip() for t in ep_info_all]
    raw_wt_title = wt_info[0]
    refine_wt_title = clear_text(raw_wt_title)

    print('------------------------------------------------------')
    print(f'<system> <{refine_wt_title}> 확인되었습니다')
    print(f'<system> 지정된 디렉토리에 <{refine_wt_title}> 폴더를 생성합니다')
    print('------------------------------------------------------')

    return refine_wt_title, pres_dir


if __name__ == '__main__':
    my_info()
    fake_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    driver_dir = os.getcwd()
    wt_id = input('<system> 웹툰의 ID를 입력해주십시오 : ')
    print('------------------------------------------------------')

    ref_wt_title, pres_dir = get_wt_title(wt_id, fake_header)

    try:
        os.mkdir(pres_dir + ref_wt_title)
    except FileExistsError:
        print('<system> 같은 이름의 디렉토리가 이미 있는 것 같습니다')
        print('<system> 해당 폴더를 삭제하고 진행합니다')
        print('------------------------------------------------------')
        try:
            shutil.rmtree(pres_dir + ref_wt_title)
        except PermissionError:
            print('<system> 다른 프로세스가 파일을 사용 중이기 때문에 프로세스가 액세스 할 수 없습니다')
            end_program()
        os.mkdir(pres_dir + ref_wt_title)
    try:
        driver = webdriver.Chrome(driver_dir + '/' + 'chromedriver.exe')
    except:
        print('<system> [ERROR] "chromedriver.exe"가 없습니다. 확인해주세요.')
        end_program()

    while True:
        print('<system> 성인 인증이 필요한 웹툰이라면 현재 열린 크롬 탭에서 네이버 접속 후 로그인을 하세요 ')
        a = input("<system> 준비가 다 되면 r을 누르세요")

        if a == "r":
            break
        else:
            print("<system> 입력받은 문자 : " + a)
    print('------------------------------------------------------')

    # requests로 로그인 정보 가져오는 코드
    s = requests.session()
    s.headers.update(fake_header)
    driver.get_cookies()

    for cookie in driver.get_cookies():
        c = {cookie['name'] : cookie['value']}
        s.cookies.update(c)

    wt_basic_url = 'https://comic.naver.com/webtoon/detail?titleId=' + wt_id + '&no='
    rem_ep_title = str()
    start_time = time.time()
    last_i = 0
    start_ep, end_ep = set_wt_area()
    for i in range(start_ep, end_ep + 1):
        # print(wt_basic_url + str(i))  # 현재 작업중인 URL
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

        make_file = open(driver_dir + '/' + 'wt_temp_file.txt', 'w', encoding='UTF-8')  # [1] 참고
        print(raw_links, file=make_file)
        make_file.close()

        temp_file = open(driver_dir + '/' + 'wt_temp_file.txt', 'r', encoding='UTF-8')
        temp_text = temp_file.read()

        find_ep_title = temp_text.split('meta')
        # raw_title : 특수문자 제거전의 에피소드 제목
        # rem_ep_title : 특수문자를 제거한 이전 에피소드의 제목
        raw_title, rem_ep_title = str(), str()
        for link in find_ep_title:
            if '"og:description' in link:
                left = link.find('nt="')
                right = link.rfind('" property="og:description"/>')
                raw_title = link[left+4:right]

        # 웹툰의 끝자락에 도달하면 break
        if rem_ep_title == raw_title or len(raw_title) > 50:
            break

        refine_title = clear_text(raw_title)
        rem_ep_title = refine_title
        # print(raw_title, rem_ep_title)
        ep_dir_title = '[' + str(i).zfill(3) + '] ' + refine_title
        os.chdir(pres_dir + ref_wt_title)
        os.mkdir(ep_dir_title)
        print(f'현재 [{str(i).zfill(3)}] {refine_title} 작업 중입니다')
        os.chdir(pres_dir + ref_wt_title + '/' + ep_dir_title)

        downloads_imgs(temp_text, fake_header)
        os.chdir('..')
        last_i = i

    clean_file = open(driver_dir + '/' + 'wt_temp_file.txt', 'w', encoding='UTF-8')  # [1] 참고
    print(' ', file=clean_file)
    clean_file.close()

    driver.close()
    get_end_time(start_time, last_i)



'''
[1] cp949' codec can't encode character '\xa0' in position 3379: illegal multibyte sequence 해결 방법 UTF 추가
'''