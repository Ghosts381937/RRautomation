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
def iselemexit(xpath):#檢測該元素是否存在 
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False
def wait(xpath):#當該xpath出現時繼續下個動作,否則等完30秒
    WebDriverWait(driver,30).until(
        EC.presence_of_element_located((By.XPATH,xpath))
    )
    time.sleep(1)
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
        while True:
            try:
                wait('//*[@id="email"]')
                email = driver.find_element_by_xpath('//*[@id="email"]')#取得輸入email框位置
                email.send_keys(username)
                pas = driver.find_element_by_xpath('//*[@id="pass"]')#取得輸入password框位置
                pas.send_keys(password)
                pas.submit()#enter
                break
            except:
                print('錯誤!重新登入中')
    #google
    elif account == 2:
        driver.find_element_by_tag_name('div.sa_sn.float_left.imp.gogo').click()
        while True:
            try:
                wait('//*[@id="identifierId"]')
                email = driver.find_element_by_xpath('//*[@id="identifierId"]')
                email.send_keys(username)
                email.send_keys(Keys.ENTER)#enter
                break
            except:
                print('錯誤!重新登入中')
        while True:
            try:
                wait('//*[@id="password"]/div[1]/div/div[1]/input')#等待下個頁面跳出
                pas = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
                pas.send_keys(password)
                pas.send_keys(Keys.ENTER)
                break
            except:
                print('錯誤!重新登入中')   
    #vk
    else:
        driver.find_element_by_xpath('//*[@id="sa_add2"]/div[2]/a[3]/div').click()
        while True:
            try:
                wait('//*[@id="login_submit"]/div/div/input[6]')
                email = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[6]')
                email.send_keys(username)
                pas = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[7]')
                pas.send_keys(password)
                pas.submit()
                break
            except:
                pass
def ispremium():#高級會員回傳1,否則回傳0
    #確保連結在遊戲主頁面
    while True:
        if(driver.current_url == 'https://rivalregions.com/#overview'):
            wait('//*[@id="header_money"]/div')
            break
    driver.find_element_by_xpath('//*[@id="header_money"]/div').click()#點擊右上角課金選項
    #獲取是否為高級會員字串
    wait('//*[@id="header_slide_inner"]/div[3]/form[3]/div[3]/div/h1')
    member = driver.find_element_by_xpath('//*[@id="header_slide_inner"]/div[3]/form[3]/div[3]/div/h1').text
    if member[0:2] == '續訂':
        print('高級會員模式.....')
    else:
        print('普通會員模式.....')
'''
def autoperk(type,isgold):
    if isgold == 0:
        pass
def howtoperk():
    while True:
        try:
            typ = int(input('請輸入欲升級的技能(1.STR 2.EDU 3.END):'))
            if typ!=1 and typ!=2 and typ!=3:
                print('錯誤輸入')
            else:
                break
        except:
            print('錯誤輸入')
    while True:
        try:
            isgold = int(input('是否使用黃金升級技能(0.NO 1.YES):'))
            if isgold!=1 and isgold!=2 and isgold!=3:
                print('錯誤輸入')
            else:
                break
        except:
            print('錯誤輸入')
    return [typ,isgold]
'''
def minegold(energy_num):
    wait('//*[@id="header_menu"]/div[9]')
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[9]').click()# 生產
    wait('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[2]')
    driver.find_element_by_xpath('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[2]').click()# 自動模式
    wait('//*[@id="header_menu"]/div[6]')
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[6]').click()# 倉庫
    wait('//*[@id="content"]/div[11]/div[3]/span')
    Enegy = driver.find_element_by_xpath('//*[@id="content"]/div[11]/div[3]/span').text# 能量飲料目前數量
    while True:
        if int(Enegy) <= 600:
            driver.find_element_by_xpath('//*[@id="content"]/div[11]').click()# 點擊飲料打開購買欄
            wait('//*[@id="storage_market"]/div[2]/div[3]/input')
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[3]/input')
            num.clear()
            num.send_keys(energy_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[4]/div').click()# 輸入並購買   
def war():
    war_type = int(input(請選擇要買哪種武器1.戰機2.月球戰車3.激光無人機：))
    war_num = int(input(購買數量：))
    wait('//*[@id="header_menu"]/div[16]')
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[16]').click() # 戰爭
    wait('//*[@id="content"]/div[4]/div[2]/div')
    driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div').click() # 軍事演習
    wait('//*[@id="send_b_wrap"]/div[3]')
    driver.find_element_by_xpath('//*[@id="send_b_wrap"]/div[3]').click() # 全自動
    driver.switch_to_alert().accept() # 訊息框確認
    wait('//*[@id="slide_close"]')
    driver.find_element_by_xpath('//*[@id="slide_close"]').click() # 返回(X)
    wait('//*[@id="header_menu"]/div[6]')
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[6]').click() # 倉庫
    wait('//*[@id="content"]/div[20]/div[3]/span')
    weapon = driver.find_element_by_xpath('//*[@id="content"]/div[20]/div[3]/span').text # 武器數量
    while True:
        if weapon <= 220:
            wait('//*[@id="content"]/div[20]')
            driver.find_element_by_xpath('//*[@id="content"]/div[20]').click() # 點擊月球戰車打開購買欄
            # 輸入並購買
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input').send_keys(war_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]').click() 
def main():
    login()
    '''
    perk = howtoperk()
    autoperk(perk[0],perk[1])
    '''
    energy_num = int(input('沒能量飲料時購買數量：'))
    while True:
        if iselemexit('//*[@id="header_my_fill_bar_countdown"]'):
            minegold(energy_num)
main()




   
