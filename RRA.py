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
driver.get('https://rivalregions.com/')
driver.maximize_window()
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
        time.sleep(1)#google帳號密碼輸入在不同頁面所以等1秒
        pas = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        pas.send_keys(password)
        pas.submit()
    #vk
    else:
        driver.find_element_by_xpath('//*[@id="sa_add2"]/div[2]/a[3]/div').click()
        email = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[6]')
        email.send_keys(username)
        pas = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[7]')
        pas.send_keys(password)
        pas.submit()
login()