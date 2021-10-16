import os
import shutil
import time
import requests
from bs4 import BeautifulSoup as bs


def my_info():
    print('------------------------------------------------------')
    print('제작자 : Ratatou2')
    print('문의 및 개선 사항은 ws4232@naver.com 으로 메일 부탁드립니다')
    print('https://github.com/Ratatou2')
    print('https://blog.naver.com/ws4232')
    print('------------------------------------------------------')


def clear_text(word):
    special_char = '\/:*?"<>|'
    return ''.join(char for char in word if char not in special_char)


def get_end_time(re_time):
    print('------------------------------------------------------')
    print('다운로드가 완료되었습니다')
    end_time = time.time() - re_time
    print(f'소요된 시간은 {round(end_time)}초 (대략 {round((end_time/60), 1)}분) 입니다\n')
    print('------------------------------------------------------')
    while True:
        print()
        a = input("q를 입력하면 프로그램은 종료됩니다")
        if a == "q":
            break
        else:
            print("입력받은 문자 : " + a)


def set_directory(directory):
    id_input = int(input('웹툰 ID를 입력하세요 : '))
    code = str(id_input)  # 네이버 웹툰의 ID를 문자열로 변경

    print('※지정된 경로에 웹툰 제목과 같은 디렉토리가 이미 있는 경우 에러가 발생합니다※')
    print(f'현재 기본 디렉토리 : [{directory}]')
    ask_input = input('기본 디렉토리를 변경하시겠습니까? (y/n) : ')

    if ask_input == 'y':
        temp = input('지정할 디렉토리를 입력해주세요 : ')
        directory = temp + '/'
    elif ask_input == 'n':
        print('기본 디렉토리를 변경하지 않습니다\n')
    else:
        print('기본 디렉토리로 강제 진행합니다')
        print('D 드라이브가 없을 경우 에러가 발생하니 프로그램을 다시 실행해주세요\n')

    try:
        os.chdir(directory)
    except:
        print('[Warning]')
        print(f'경로 [ {directory} ]가 확인되지 않습니다.')
        print(f'[ C:/ ]로 경로를 변경합니다')
        directory = 'C:/'

    return code, directory


def get_wt_title(wt_code, wt_dir):

    # 웹툰 제목 따오기 위한 부분
    html = requests.get(part_URL + wt_code, headers=fake_header)
    title_soup = bs(html.text, 'html.parser')
    wt_name = title_soup.select_one('#sectionContWide > div.comicinfo > div.detail > h2')
    wt_info = [t for t in wt_name]

    wt_title = wt_info[0]
    print('------------------------------------------------------')
    print(f'<{wt_title}> 확인되었습니다')
    print(f'지정된 디렉토리에 <{wt_title}> 폴더를 생성합니다')
    print('------------------------------------------------------')

    # 웹툰 제목의 폴더를 지정한 경로에 생성
    if not os.path.exists(wt_dir + wt_title):
        os.mkdir(wt_dir + wt_title)
    else:
        print('같은 이름의 디렉토리가 이미 있는 것 같습니다')
        print('확인하고 재실행해주세요')

    # 생성한 웹툰 제목의 폴더로 이동
    os.chdir(wt_dir + wt_title)

    return wt_code, wt_title, wt_dir


# 웹툰 회차 지정 기능
def set_wt_area():
    print('<받고 싶은 회차를 다음 예시와 같이 입력해주세요>')
    print('ex) 7화 한개만 받고 싶은 경우       -> "7~7"  을 입력')
    print('ex) 2화부터 30화까지 받고 싶은 경우 -> "2~30"  을 입력')
    print('ex) 50화부터 끝까지 받고 싶은 경우  -> "50~1000" 을 입력')
    print('ex) 별도의 지정없이 전 회차 다운 받고 싶은 경우 -> 그냥 엔터')

    try:
        start_ep, end_ep = map(int, input().split('~'))
    except ValueError:
        start_ep, end_ep = 1, 1000

    return start_ep, end_ep


# 한 웹툰의 모든 회차를 조회 & 회차 제목 가져오는 코드
def wt_download(wt_code, wt_title, wt_dir):
    begin_time = time.time()
    prev_wt_name = str()

    start_ep, end_ep = set_wt_area()
    for i in range(start_ep, end_ep + 1):
        URL = part_URL + wt_code + '&no=' + str(i)
        html = requests.get(URL, headers=fake_header)
        soup = bs(html.text, 'html.parser')

        ep_info_all = soup.select('#sectionContWide > div.tit_area > div.view > h3')
        ep_info = [t for t in ep_info_all]
        try:
            ep_title = str(ep_info[0])
        except:
            break

        ep_first_name = ep_title.find('>')
        ep_last_name = ep_title.find('</')
        ep_name = ep_title[ep_first_name+1:ep_last_name]

        # ep_titile에 폴더 만들수 없는 특수문자 들어간 경우 처리
        ep_name = clear_text(ep_name)

        if ep_name == prev_wt_name:
            break

        ep_title = '[' + str(i).zfill(3) + '] ' + ep_name
        os.mkdir(ep_title)
        print(f'현재 [{str(i).zfill(3)}] {ep_name} 작업 중입니다')
        os.chdir(wt_dir + wt_title + '/' + ep_title)

        # 한 화의 모든 사진을 받는 코드
        tag_soup = soup.select('#comic_view_area > div.wt_viewer')  # 링크 추출은 크롬 우클릭 > copy > sector
        file_name_count = 1
        for sep in tag_soup:
            for img in sep:
                reform = str(img)
                if reform != '\n':
                    src_position = reform.find('return false" src="http')
                    title_position = reform.rfind('title=""/>')
                    ep = reform[src_position+19:title_position-2]
                    file_name = str(file_name_count).zfill(fill_zero)

                    # print(ep[40:46] == str(wt_code))
                    if ep[40:46] == wt_code:  # 웹툰 ID가 같을 경우에만 다운
                        ep_html = requests.get(ep, headers=fake_header)
                        with open(file_name + file_ext, 'wb+') as f:
                            f.write(ep_html.content)
                    else:pass

                    print(f'{file_name_count} 번째 사진 작업중', end='\r', flush=True)
                    file_name_count += 1

        os.chdir('..')  # 한 회차를 다 받았으니 상위 경로로 이동
        prev_wt_name = ep_name

    return begin_time


if __name__ == '__main__':
    fill_zero = 3  # 파일명 앞에 0 몇개 채울건지?
    file_ext = '.png'  # 파일 확장자 뭐로 할건지?
    main_directory = 'D:/'  # 사진 저장할 메인 디렉토리
    fake_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    part_URL = 'https://comic.naver.com/webtoon/detail?titleId='  # 네이버 웹툰 기본 주소

    my_info()
    get_wt_id, get_dir = set_directory(main_directory)
    A, B, C = get_wt_title(get_wt_id, get_dir)
    start_time = wt_download(A, B, C)

    get_end_time(start_time)

