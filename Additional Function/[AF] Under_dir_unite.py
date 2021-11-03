import os, shutil, time


def my_info():
    print('------------------------------------------------------')
    print('제작자 : Ratatou2')
    print('문의 및 개선 사항은 ws4232@naver.com 으로 메일 부탁드립니다')
    print('https://github.com/Ratatou2')
    print('https://blog.naver.com/ws4232')
    print('------------------------------------------------------')
    print("<< 유의사항 >>\n")
    print('이 프로그램 "N_wt_downloader"의 추가적인 기능을 목적으로 만들어졌습니다')
    print('이 프로그램의 목적은 입력하신 경로 하위의 모든 폴더에서 사진을 꺼내와 한 폴더에 통합하는데 있습니다')
    print('"N_wt_downloader"를 사용한 이후 모든 사진의 통합이 필요할 때만 사용하십시오')
    print('폴더에 "[웹툰 이름] 통합본"이란 폴더가 존재하면 이 코드는 작동하지 않습니다')
    print('------------------------------------------------------')


def under_dir_unite():
    work_dir = input('통합할 파일이 있는 곳의 주소를 붙여넣으세요 : ')

    work_list = os.listdir(work_dir)
    wt_title = work_dir[work_dir.rfind('/')+1:]

    os.mkdir(wt_title + ' 통합본')

    count = 1
    for ep in work_list:
        ep_dir = work_dir + '/' + ep
        ep_img_list = os.listdir(ep_dir)
        for img in ep_img_list:
            exp = img[-4:]
            shutil.move(ep_dir + '/' + img, wt_title + ' 통합본' + '/' + str(count).zfill(5) + exp)
            count += 1
        os.rmdir(work_dir + '/' + ep)

    return count


if __name__ == '__main__':
    my_info()
    print(f'{under_dir_unite()}장 이동 완료했습니다')
    print('이 프로그램은 10초 후에 종료됩니다')
    time.sleep(10)
