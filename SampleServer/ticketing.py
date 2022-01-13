import sys, os, time, threading
from os import path
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

base_dir = path.dirname(path.abspath(__file__))

from fastapi import FastAPI

#WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


from Database.conn import database
from APIServer.app.common.config import config



import time
import random
from playsound import playsound
from getpass import getpass
from datetime import datetime

#SMTP
import smtplib
from email.mime.text import MIMEText
 


def initial_webdriver_chrome():
    #BackGround로 실행할지에 대한 Option 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("headless")

    #webdriver 생성 
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options) #driverManger에서 생성
    #driver = webdriver.Chrome(f'{base_dir}/chromedriver',options=options) #driverManger에서 생성
    return driver

def initial_webdriver_firefox():
    #BackGround로 실행할지에 대한 Option 설정
   options = Options()
   options.add_argument('--headless') # EN SEGUNDO PLANO, SIN GUI
   driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', options=options)
   return driver



def send_smtp():
    #SMTP 설정
    sendEmail = "azxc1749@gmail.com"
    recvEmail = "azxc1749@gmail.com"
    password = "dtbzkfigzjqdfahh"  #구글 비밀번호가 아니라 구글 APP 비밀번호 16자리
    smtpName = "smtp.gmail.com" #smtp 서버 주소
    smtpPort = 587 #smtp 포트 번호

    #본문
    text = "SRT 예약이 완료 되었습니다. \n   - 날짜 : {} \n   - 내용 : {} -> {} \n SRT App에 진입하여 발권 진행이 필요합니다. \n https://play.google.com/store/apps/details?id=kr.co.srail.newapp".format(infoMap['출발날짜'], infoMap['출발정보'],infoMap['도착정보'])
    msg = MIMEText(text) #MIMEText(text , _charset = "utf8")

    #메일제목
    msg['Subject'] ="[SRT] {} {} -> {} 예약 완료".format(infoMap['출발날짜'],infoMap['출발정보'], infoMap['도착정보'])
    msg['From'] = sendEmail
    msg['To'] = recvEmail

    s=smtplib.SMTP( smtpName , smtpPort ) #메일 서버 연결
    s.starttls() #TLS 보안 처리
    s.login( sendEmail , password ) #로그인
    s.sendmail( sendEmail, recvEmail, msg.as_string() ) #메일 전송, 문자열로 변환하여 보냅니다.
    s.close() #smtp 서버 연결을 종료합니다.
    return



#시간 설정값
start_time = time.time() 
restcheck_time = random.randrange(600,900)
rest_time = random.randrange(300,420)

#정보저장 Map 전역변수 생성
infoMap = dict()


def playsound_fanfare():
    playsound("fanfare.mp3")
    return


def initial_timer():
    start_time = time.time() 
    now = datetime.now()
    print("시작시간을 초기화 합니다. 현재시간 [{}:{}:{}]".format(now.hour, now.minute, now.second))

    restcheck_time = random.randrange(600,900)
    print("휴식 조건 시간을 {}초로 초기화 합니다.".format(restcheck_time))

    rest_time = random.randrange(300,420)
    print("휴식 시간을 {}초로 초기화 합니다.".format(restcheck_time))

    return

def initial_vaule():
    
    #infoMap['로그인유형'] = input("로그인유형 (1=회원번호, 2=이메일, 3=모바일) : ")
    infoMap['아이디'] = input("아이디 입력 : ")
    infoMap['비밀번호'] = getpass("비밀번호 입력 : ")
    infoMap['출발지'] = input("출발지 : ")
    infoMap['목적지'] = input("목적지 : ")
    infoMap['출발날짜'] = input("출발날짜(yyyymmdd) : ")
    infoMap['출발시간'] = input("출발시간(hh) : ")
    infoMap['마감시간'] = input("마감시간(hh) : ")
    return infoMap


def run_ticketing():
    initial_vaule()
    initial_timer()

    driver = initial_webdriver_chrome()
    
    #재시도 횟수
    retryCnt = 1

    #로그인 창으로 이동
    driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
    driver.implicitly_wait(20) # 페이지 다 뜰 때 까지 기다림
    time.sleep(1)

    # 휴대폰번호 로그인 입력 [참고] 로그인 유형에 따른 ID,PW, 클릭버튼의 xml Path가 달라짐
    driver.find_element(By.XPATH, '//*[@id="srchDvCd3"]').click()  #휴대폰 번호
    driver.find_element(By.ID, 'srchDvNm03').send_keys(infoMap['아이디']) # 휴대폰 번호
    driver.find_element(By.ID, 'hmpgPwdCphd03').send_keys(infoMap['비밀번호']) # 비밀번호

    # 로그인 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[4]/div/div[2]/input').click()
    driver.implicitly_wait(20)
    time.sleep(1)

    # 기차 조회 페이지로 이동
    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
    driver.implicitly_wait(20)
    time.sleep(1)

    # 출발지 입력
    dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
    dep_stn.clear() 
    dep_stn.send_keys(infoMap['출발지'])

    # 도착지 입력
    arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
    arr_stn.clear()
    arr_stn.send_keys(infoMap['목적지'])

    # 출발날짜
    elm_dptDt = driver.find_element(By.ID, "dptDt")
    driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)
    Select(driver.find_element(By.ID,"dptDt")).select_by_value(infoMap['출발날짜'])

    # 출발시간
    elm_dptTm = driver.find_element(By.ID, "dptTm")
    driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
    Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text(infoMap['출발시간'])

    # 조회 버튼 클릭
    driver.find_element(By.XPATH,"//input[@value='조회하기']").click()
    
    isReserved = False
    while True:
        #3~5초 랜덤 기다리기
        time.sleep(random.uniform(3, 6))

        #10~15 사이 동안 안되면 5분정도 쉬고 다시 진행
        running_time_sec = time.time() - start_time
        if running_time_sec > restcheck_time :
            print("현재 {}초 동안 실행하여 감지회피를 위해 {}초 동안 휴식후 재진행 합니다. ".format(running_time_sec,rest_time))
            time.sleep(rest_time)
            initial_timer()
            

        train_list = driver.find_elements(By.CSS_SELECTOR, '#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr')
        for i in range(1, len(train_list)+1):
            # 3=열차번호
            infoMap['열차번호'] = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(3)").text.replace("\n"," ")
            
            # 4=출발역(시간)
            infoMap['출발정보'] = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(4)").text.replace("\n"," ")
            dep_stn = infoMap['출발정보'].split(' ')[0]
            dep_time = infoMap['출발정보'].split(' ')[1]
            
            # 5=도착역(시간)
            infoMap['도착정보'] = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(5)").text.replace("\n"," ")
            arr_stn = infoMap['도착정보'].split(' ')[0]
            arr_time = infoMap['도착정보'].split(' ')[1]
    
            # 6=특실
            special_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(6)").text.replace("\n"," ")
            
            # 7=일반실
            standard_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text.replace("\n"," ")
    
            if dep_time.split(':')[0] < infoMap["마감시간"] :
                if "예약하기" in standard_seat:  
                    driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{i}]/td[7]/a/span").click()
                    
                    if "confirmReservationInfo" in driver.current_url:
                        isReserved = True
                        playsound_fanfare()
                        send_smtp()
                        print('예약이 완료되었습니다.')
                        break
                    else:
                        print("예약하기에 실패하였습니다. 좌석이 없거나 출발시간이 지난 상태")
                        break
            elif dep_time.split(':')[0] > infoMap["마감시간"] :
                break

        if not isReserved:
            # 다시 조회하기
            submit = driver.find_element(By.XPATH, "//input[@value='조회하기']")
            driver.execute_script("arguments[0].click();", submit)

            now = datetime.now()
            print("[{}:{}:{}] 예약이 가능한 시간이 없어 새로고침을 진행합니다. 재시도 : {} 번".format(now.hour, now.minute, now.second, retryCnt))
            retryCnt += 1

        else:
            break

    return























