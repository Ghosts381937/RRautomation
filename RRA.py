from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import getpass
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://rivalregions.com/')
def wait(path):#當該xpath出現時繼續下個動作,否則等完100秒
    WebDriverWait(driver,100).until(
        EC.presence_of_element_located((By.XPATH,path))
    )
def login():
    while True:
        try:
            account = int(input('請輸入帳號類型(1.FB 2.Google 3.VK):'))
            #避免輸入123以外的數字
            if account!=1 and account!=2 and account!=3:
                print('錯誤輸入')
            else:
                break
        #避免輸入數字以外的字串
        except:
            print('錯誤輸入')
    username = input('請輸入帳號:')
    password = getpass.getpass('請輸入密碼:')
    #fb
    if account == 1:
        driver.find_element_by_tag_name('div.sa_sn.imp.float_left').click()#點選fb登入
        email = driver.find_element_by_xpath('//*[@id="email"]')#取得輸入email框位置
        email.send_keys(username)
        pas = driver.find_element_by_xpath('//*[@id="pass"]')#取得輸入password框位置
        pas.send_keys(password)
        pas.submit()#enter
    #google
    elif account == 2:
        driver.find_element_by_tag_name('div.sa_sn.float_left.imp.gogo').click()
        email = driver.find_element_by_xpath('//*[@id="identifierId"]')
        email.send_keys(username)
        email.send_keys(Keys.ENTER)#enter
        wait('//*[@id="password"]/div[1]/div/div[1]/input')#google帳號密碼輸入在不同頁面所以等待
        pas = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        pas.send_keys(password)
        pas.send_keys(Keys.ENTER)
    #vk
    else:
        driver.find_element_by_xpath('//*[@id="sa_add2"]/div[2]/a[3]/div').click()
        email = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[6]')
        email.send_keys(username)
        pas = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[7]')
        pas.send_keys(password)
        pas.submit()
def ispremium():#高級會員回傳1,否則回傳0
    #確保連結在遊戲主頁面
    while True:
        if(driver.current_url == 'https://rivalregions.com/#overview'):
            wait('//*[@id="header_money"]/div')
            break
    driver.find_element_by_xpath('//*[@id="header_money"]/div').click()
    wait('//*[@id="header_slide_inner"]/div[3]/form[3]/div[3]/div/h1')
    member = driver.find_element_by_xpath('//*[@id="header_slide_inner"]/div[3]/form[3]/div[3]/div/h1').text
    if member[0:2] == '續訂':
        print('高級會員模式.....')
    else:
        print('普通會員模式.....')
login()

