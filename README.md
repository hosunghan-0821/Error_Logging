# Error_Logging

## 프로젝트 개요
### 소개
* 항해99를 진행하면서, 발생했던 에러와 그 에러의 해결과정을 공유하는 사이트
* [시연영상] (https://youtu.be/zvuuU9d92Eg)

### 기간 및 팀원
* 제작기간 2022.07.11 ~2022.07.14
* 개발팀원 : 한호성, 김진무, 은예찬
---
## 와이어프레임



### 로그인 및 회원가입
![image](https://user-images.githubusercontent.com/79980357/179387853-88651901-1ba4-4850-af00-29d8df523cdb.png)

![image](https://user-images.githubusercontent.com/79980357/179387939-647ac332-635b-4b26-a2ea-516ffd046239.png)

### 메인 페이지
![image](https://user-images.githubusercontent.com/79980357/179387977-bd6f6203-334c-472a-9ed6-467eb985c8ab.png)

### 게시글 상세보기
![image](https://user-images.githubusercontent.com/79980357/179388000-40072718-50ad-4d04-8b1b-2cab9caa61d8.png)

## 기술스택

---
### Frontend
<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> 
<img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white">
  <img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">

### Backend

<img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
<img src="https://img.shields.io/badge/mongoDB-47A248?style=for-the-badge&logo=MongoDB&logoColor=white">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 

### Deploy

  <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"> 


## TroubleShooting

---
<br>
1. 깃허브 협업시 Conflict를 줄이기 위한 고민 <BR>
    -Flask에 내장된 Blueprint 라이브러리 활용 / API 기능별로 파일분리해서 코드작성

![image](https://user-images.githubusercontent.com/79980357/179388469-0e040caa-ccef-43d9-9466-0bdb17f81e91.png)<br>

2. 이미지 업로드 및 DB 처리 방식에 대한 고민 <Br> 
  -DB에 직접 이미지 저장 <BR>
  -서버에 이미지 저장 후, DB에 이미지에 접근할 수 있는 경로 저장  ✅

![image](https://user-images.githubusercontent.com/79980357/179388480-5013fd5f-bb3f-4328-9038-103c436388f0.png)


