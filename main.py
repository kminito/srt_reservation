# -*- coding: utf-8 -*-
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def open_brower():
    driver = webdriver.Chrome("chromedriver")
    return driver


def login(driver, login_id, login_psw):
    driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
    driver.implicitly_wait(15)
    driver.find_element(By.ID, 'srchDvNm01').send_keys(str(login_id))
    driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(str(login_psw))
    driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
    driver.implicitly_wait(5)
    return driver


def search_train(driver, dpt_stn, arr_stn, dpt_dt, dpt_tm, num_trains_to_check=2, want_reserve=False):
    """
    Search train and refresh until tickets are available.

    :param driver: Selenium Webdriver
    :param dpt_stn: SRT 출발역
    :param arr_stn: SRT 도착역
    :param dpt_dt: 출발 날짜 YYYYMMDD 형태 ex) 20220115
    :param dpt_tm: 출발 시간 hh 형태, 반드시 짝수 ex) 06, 08, 14, ...
    :param num_trains_to_check: 검색 결과 중 예약 가능 여부 확인할 기차의 수 ex) 2일 경우 상위 2개 확인
    :param want_reserve: 예약 대기가 가능할 경우 선택 여부
    :return: Selenium Webdriver

    입력한 기차역은 아래 리스트에 있어야 함.
    station_list = ["수서", "동탄", "평택지제", "천안아산", "오송", "대전", "김천(구미)", "동대구",
                "신경주", "울산(통도사)", "부산", "공주", "익산", "정읍", "광주송정", "나주", "목포"]
    """

    is_booked = False  # 예약 완료 되었는지 확인용
    cnt_refresh = 0  # 새로고침 회수 기록

    # 기차 조회 페이지로 이동
    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
    driver.implicitly_wait(5)
    # 출발지/도착지 입력
    elm_dpt_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
    elm_dpt_stn.clear()
    elm_dpt_stn.send_keys(dpt_stn)
    elm_arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
    elm_arr_stn.clear()
    elm_arr_stn.send_keys(arr_stn)

    # 출발 날짜
    elm_dptDt = driver.find_element(By.ID, "dptDt")
    driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)
    Select(driver.find_element(By.ID, "dptDt")).select_by_value(dpt_dt)

    # 출발 시간
    elm_dptTm = driver.find_element(By.ID, "dptTm")
    driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
    Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text(dpt_tm)

    print("기차를 조회합니다")
    print(f"출발역:{dpt_stn} , 도착역:{arr_stn}\n날짜:{dpt_dt}, 시간: {dpt_tm}시 이후\n{num_trains_to_check}개의 기차 중 예약")
    print(f"예약 대기 사용: {want_reserve}")

    # 조회하기 버튼 클릭
    driver.find_element(By.XPATH, "//input[@value='조회하기']").click()
    driver.implicitly_wait(5)
    time.sleep(1)

    while True:
        for i in range(1, num_trains_to_check+1):
            standard_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text
            reservation = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8)").text

            if "예약하기" in standard_seat:
                print("예약 가능 클릭")
                driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7) > a").click()
                driver.implicitly_wait(3)

                if driver.find_elements(By.ID, 'isFalseGotoMain'):
                    is_booked = True
                    print("예약 성공")
                    break
                else:
                    print("잔여석 없음. 다시 검색")
                    driver.back()  # 뒤로가기
                    driver.implicitly_wait(5)

            if want_reserve:
                if "신청하기" in reservation:
                    print("예약 대기 완료")
                    driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8) > a").click()
                    is_booked = True
                    break

        if not is_booked:
            time.sleep(randint(2, 4))  #2~4초 랜덤으로 기다리기

            # 다시 조회하기
            submit = driver.find_element(By.XPATH, "//input[@value='조회하기']")
            driver.execute_script("arguments[0].click();", submit)
            cnt_refresh += 1
            print(f"새로고침 {cnt_refresh}회")
            driver.implicitly_wait(10)
            time.sleep(0.5)
        else:
            break
    return driver


if __name__ == "__main__":
    import os
    srt_id = os.environ.get('srt_id')
    srt_psw = os.environ.get('srt_psw')

    driver = open_brower()
    driver = login(driver, srt_id, srt_psw)
    search_train(driver, "동탄", "동대구", "20220115", "08", num_trains_to_check=2, want_reserve=False)
