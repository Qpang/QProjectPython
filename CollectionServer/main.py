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

from Database.schema import Assets, Notice
from Database.conn import database
from APIServer.app.common.config import config

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


def xangle():
    driver = initial_webdriver_firefox()
    
    while True :
        if len(driver.window_handles) > 1 :
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            
        driver.execute_script('window.open("about:blank", "_blank");')
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('https://xangle.io/disclosure-feed?exchange=all')



        notice_info = dict()

        notice_info['currency'] = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/span[1]").text.split('\n')     
        notice_info['title'] =driver.find_element(By.XPATH, f"/html/body/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[2]").text
        notice_info['reg_date'] =driver.find_element(By.XPATH, f"/html/body/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[3]").text
                
        #URL 확인하기 위한 작업 진행
        driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div/div[2]/button").click()
        driver.find_element(By.XPATH, f"/html/body/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div/div[2]/div").click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.implicitly_wait(20)
                
        notice_info['link'] =driver.current_url
        #link = "test"        
        # 현재 탭 닫기
        driver.close()

        # 맨 처음 탭으로 변경(0번 탭)
        driver.switch_to.window(driver.window_handles[1])
        
        notice = Notice.filter(currency = notice_info['currency'], title=notice_info['title']).first()
        if not notice:
            Notice.create(auto_commit=True, **notice_info)
        time.sleep(10)
    return

def klayswap():
    driver = initial_webdriver_firefox()
    
    driver.get('https://klayswap.com/assets')
    driver.implicitly_wait(20)
    
    while True :
        #0초에 시작한다
        while datetime.now().second!=0:
            time.sleep(0.1)
            
        coininfo_list = driver.find_elements(By.CSS_SELECTOR , '#app > main > div > section > article.asset-page__list__content > div > div')
        for item in coininfo_list:
            coininfo = item.text.split('\n')
            
            coin_info = dict()
            coin_info['currency'] = coininfo[1]
            coin_info['name_kor'] = coininfo[0]
            coin_info['price'] = coininfo[3].split(' ')[1]
            
            assets = Assets.filter(currency = coin_info['currency'])
            if not assets.first():
                Assets.create(auto_commit=True, **coin_info)
            else:
                assets.update(auto_commit=True, **coin_info)
        time.sleep(40)
        driver.refresh()
        driver.implicitly_wait(20)
    return

if __name__ == "__main__":
    app = FastAPI()
    database.init_app(app,**config())

    xangle_thread = threading.Thread(target=xangle)
    xangle_thread.start()

    klayswap_thread = threading.Thread(target=klayswap)
    klayswap_thread.start()