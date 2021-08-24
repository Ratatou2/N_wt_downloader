import os
import time
import requests
from bs4 import BeautifulSoup as bs

start_time = time.time()

fill_zero = 3  # 파일명 앞에 0 몇개 채울건지?
file_ext = '.png'  # 파일 확장자 뭐로 할건지?
main_directory = 'D:/'  # 사진 저장할 메인 디렉토리
fake_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
part_URL = 'https://comic.naver.com/webtoon/detail?titleId='  # 네이버 웹툰 기본 주소

user_input = int(input('다운받고 싶은 웹툰의 ID를 입력하세요 : '))
wt_code = str(user_input)  # 네이버 웹툰의 ID를 문자열로 변경


# 웹툰 제목 따오기 위한 부분
html = requests.get(part_URL + wt_code, headers=fake_header)
title_soup = bs(html.text, 'html.parser')
wt_name = title_soup.select_one('#sectionContWide > div.comicinfo > div.detail > h2')
wt_info = [t for t in wt_name]
wt_title = wt_info[0]


# 웹툰 제목의 폴더를 지정한 경로에 생성
try:
    if not os.path.exists(main_directory + wt_title):
        os.mkdir(main_directory + wt_title)
except OSError:
    print("Error" + main_directory + wt_title)


# 생성한 웹툰 제목의 폴더로 이동
os.chdir(main_directory + wt_title)


# 한 웹툰의 모든 회차를 조회 & 회차 제목 가져오는 코드
prev_wt_name = str()
for i in range(1, 1000):
    URL = part_URL + wt_code + '&no=' + str(i)
    html = requests.get(URL, headers=fake_header)
    soup = bs(html.text, 'html.parser')

    ep_info_all = soup.select('#sectionContWide > div.tit_area > div.view > h3')
    ep_info = [t for t in ep_info_all]
    try:
        ep_title = str(ep_info[0])
    except:
        print('STOP (있는 목록 전부 가져왔음!)')
        break

    ep_first_name = ep_title.find('>')
    ep_last_name = ep_title.find('</')
    ep_name = ep_title[ep_first_name+1:ep_last_name]

    if ep_name == prev_wt_name:
        print('끝났습니다!')
        break

    ep_title = '[' + str(i).zfill(3) + '] ' + ep_name
    os.mkdir(ep_title)
    print(f'현재 [{str(i).zfill(3)}] {ep_name} 작업 중입니다')
    os.chdir(main_directory + wt_title + '/' + ep_title)

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

                file_name_count += 1

    os.chdir('..')  # 한 회차를 다 받았으니 상위 경로로 이동
    prev_wt_name = ep_name

end_time = time.time() - start_time
print(f'소요된 시간은 {round(end_time)}초 (대략 {round(end_time)/60}분) 입니다')