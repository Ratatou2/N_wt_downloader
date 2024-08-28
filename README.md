# [📚 Project] N_wt_downloader
---
네이버 웹툰을 다운로드 해주는 프로그램
(This program  downloads webtoons on Naver)

## [프로젝트 폐기 사유]
- 불법 사이트 유통 가능성을 고려하지 못하였음
- 개발 취지와는 다른 목적으로 사용될 수 있음을 고려하여 폐기
- https://blog.naver.com/ratatou2_/222482194890

## 업데이트(update)
---
### [2021.10.16] N_wt_downloader 1.0.3 업데이트 내역
- 회차 지정하여 다운로드하는 기능 추가
- 기본 지정된 D:/ 경로가 없을 경우 자동으로 C:/ 경로로 바뀌도록 변경

### [2021.09.10] N_wt_downloader 1.0.2 업데이트 내역
- 폴더 생성에 사용할 수 없는 특수문자 제거 기능 추가('/:*?"<>|)
- 다운로드 완료시 가끔 완료 알림 1번 이상 뜨던 문제 해결

### [2021.08.25] N_wt_downloader 1.0.1 업데이트 내역
- 시간 경과후 종료가 아닌, q를 입력해야 프로그램이 종료되도록 설정
- 다운로드 소요 시간 측정 코드 수정
- 안내문 변경
- 블로그에 사용 방법 업로드
- 유의사항 작성

### [2021.08.24] N_wt_downloader 1.0.0 업데이트 내역
- 유저의 input 받을 수 있도록 코드 변경
- 디렉토리 지정 가능
- exe 파일에 맞도록 결과 출력 코드 수정

### 추가 개선점
- 원하는 회차 지정 다운로드
- 누락된 파일이 있어서 재다운로드 하고 싶은경우 있는 파일 제외하고 다운받기
- 로그인이 필요한 경우 각자 홈페이지 쿠키 사용해서 자동 로긴후 받기
- 멀티 프로세싱 이용해서 작업 속도 개선해보기

## 특징(Features)
---
- 네이버 웹툰의 제목 폴더를 생성 후 각 에피소드 별로 개별 저장
- 분당 17회차 정도 다운로드

![image](https://user-images.githubusercontent.com/61686603/134801185-c4452e9b-af8f-4387-8c07-bb56101354f7.png)


## 사용법(How to use)
----
[![BLOG](https://user-images.githubusercontent.com/61686603/135449625-8fa1d72e-2ed4-4f80-9f69-490b558561b2.png)](https://blog.naver.com/ws4232/222482194890)


**First** : 일단 프로그램을 키면 이런 화면이 나온다
![image](https://user-images.githubusercontent.com/61686603/134801219-7ff581c7-81ce-4861-8143-cce46632cbfa.png)
- 웹툰 ID를 입력하라는 것은 아래 사진의 동그라미를 의미한다
- 모든 네이버 웹툰은 고유 ID가 있어서 해당 ID가 전부 다르다
- ![image](https://user-images.githubusercontent.com/61686603/134801226-c2f5e3c9-311f-474d-b964-d1b49a42814c.png)
- 해당 ID를 입력하면 된다
- 가끔 cmd 창이 까맣게 되고 아무것도 안나올 때가 있는데 그냥 숫자 입력하면 나옵니당


**Second** : 입력하면 기본 디렉토리를 지정할 수 있다
![image](https://user-images.githubusercontent.com/61686603/134801260-f2745cec-0c9e-4ffa-99a9-95b62fe640b8.png)

- 기본 세팅은 D:/로 되어있고 y or n의 입력으로 디렉토리를 유지 또는 변경 할 수 있다
- 디렉토리 변경시엔 그냥 y 입력후 원하는 경로를 입력해주면 된다
- 그럼 해당 경로에 웹툰 제목으로 폴더를 자동으로 생성해서 그 폴더 안에 모든 회차를 다운받는다
- ※ 해당 경로에 이미 웹툰 제목과 같은 폴더가 있을 경우 다운로드는 진행되지 않음을 유의할 것

**Third** : 그렇게 다운 받으면 웹툰 제목과 함께 다운로드가 시작된다
![image](https://user-images.githubusercontent.com/61686603/134801266-9aab79a3-2f66-414f-8d64-5160b017f66d.png)
- 가끔 다운을 받다가 00번째 사진에서 다운로드가 넘어가지 않고 대기 중인 경우가 있는데 기다리면 넘어간다
- 아마 코드가 미흡해서 그런게 아닌가... 싶기도 하고 우리집 네트워크가 조금 느려서 일수도 있다
- 그러니 그냥 이 프로그램은 돌려놓고 다른 일을 하시는 것을 추천

**Fourth** : 다운로드가 완료되면 다운로드에 소요된 시간과 종료를 알린다
![image](https://user-images.githubusercontent.com/61686603/134801283-9a6ac168-a047-46a6-80bf-b7ff4dfff5d2.png)

## 주의사항(Caution)
----
![image](https://user-images.githubusercontent.com/61686603/134801439-6ad3e838-1625-42f9-a5ad-7ddee59fae58.png)
- 여기서 **주의사항**이 있는데 해당 경로에 이름이 겹치는 파일이 있다면, 이 코드는 동작하지 않는다
- 예를들어 내가 1~100 으로 설정하길 바라는데, 해당 경로에 이미 1~100 사이의 숫자를 가진 파일이 하나라도 있다면 에러가 난다
- 이럴땐 임의의 숫자를 입력하면된다
- 예를들어 123456를 입력하면 첫 파일 이름이 123456으로 설정되고 그 이후로 1씩 커지면서 저장된다
- 그러고난 후에 다시 이 코드를 똑같이 동작시켜서 1을 입력하면 해결된다
- 한줄 요약 : 에러나면 엄청 큰 임의의 숫자 하나 입력하고, 다시 돌리면 9할은 해결된다
- 이름이 같은 파일을 처리하는 코드가 없어서 생기는 에러 ㅠ

## AF(Additional Function)
----

**Under_dir_unite**
[![BLOG](https://user-images.githubusercontent.com/61686603/135449625-8fa1d72e-2ed4-4f80-9f69-490b558561b2.png)](https://blog.naver.com/ws4232/222501619886)

- 다운 받은 웹툰의 모든 폴더를 한 폴더로 통합

