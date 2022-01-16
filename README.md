# Python program for booking SRT ticket.


매진된 SRT 표의 예매를 도와주는 파이썬 프로그램입니다.  
원하는 표가 나올 때 까지 새로고침하여 예약을 시도합니다.

  
## 필요
- 파이썬 3.7에서만 테스트 진행함
- Chromedriver -> srt_reservation/main.py에서 별도 경로 설정 필요
- Selenium

## Arguments

    dpt_stn: SRT 출발역
    arr_stn: SRT 도착역
    dpt_dt: 출발 날짜 YYYYMMDD 형태 ex) 20220115
    dpt_tm: 출발 시간 hh 형태, 반드시 짝수 ex) 06, 08, 14, ...
    num_trains_to_check: 검색 결과 중 예약 가능 여부 확인할 기차의 수
    want_reserve: 예약 대기가 가능할 경우 선택 여부

    station_list = ["수서", "동탄", "평택지제", "천안아산", "오송", "대전", "김천(구미)", "동대구",
    "신경주", "울산(통도사)", "부산", "공주", "익산", "정읍", "광주송정", "나주", "목포"]


## Quick Start

```cmd
python quickstart.py --user 아이디 --psw 비밀번호 --dpt 동탄 --arr 동대구 --dt 20220118 --tm 08
```




## 예제

**Example 1)**  
동탄 -> 동대구, 2022년 01월 17일 오전 8시 이후 기차  
검색 결과 중 상위 2개가 예약 가능할 경우 예약

- srt_id는 SRT 홈페이지 로그인시 사용하는 회원 번호(10자리)입니다.

```py
if __name__ == "__main__":
    srt_id = os.environ.get('srt_id')
    srt_psw = os.environ.get('srt_psw')

    srt = SRT("동탄", "동대구", "20220117", "08")
    srt.run(srt_id, srt_psw)
```  
  
  
  
**Example 2)**  
예약 대기 버튼 사용  
검색 결과 중 상위 3개 예약 가능 여부 확인  
```python
srt = SRT("동탄", "동대구", "20220117", "08", num_trains_to_check=3, want_reserve=False)
srt.run(srt_id, srt_psw)
```
- 예약 대기란? : 예약대기는 해당 열차가 출발하기 3일 전까지 매일 접수하여 다음날 오전9시 취소표를 배정하며, 출발 2일 전부터는 접수하지 않음  



**실행 결과**

![](./img/img1.png)

## 기타  
명절 승차권 예약에는 사용이 불가합니다.