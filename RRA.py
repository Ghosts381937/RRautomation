from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import getpass
import math
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
        return 1
    else:
        print('普通會員模式.....')
        return 0
def getchainfo():#get角色資料
    driver.get('https://rivalregions.com/')
    lv = int(driver.find_element_by_xpath('//*[@id="index_exp_level"]').text)
    strn = int(driver.find_element_by_xpath('//*[@id="index_perks_list"]/div[4]/div[2]').text)
    edu = int(driver.find_element_by_xpath('//*[@id="index_perks_list"]/div[5]/div[2]').text)
    end = int(driver.find_element_by_xpath('//*[@id="index_perks_list"]/div[6]/div[2]').text)
    return {'lv':lv,'str':strn,'edu':edu,'end':end}
def single_costenergy(end):#單次派兵消耗能量
    if end <50:
        return 9
    elif end<75:
        return 8
    elif end<100:
        return 7
    else:
        return 6
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
def autoperk(type,isgold):
    skill = ['//*[@id="index_perks_list"]/div[4]/div[1]','//*[@id="index_perks_list"]/div[5]/div[1]','//*[@id="index_perks_list"]/div[6]/div[1]']#技能元素位置
    ornot_gold = ['//*[@id="perk_target_4"]/div[1]/div[1]/div','//*[@id="perk_target_4"]/div[2]/div[1]/div']#是否用金升技能個別位置
    driver.get('https://rivalregions.com/')
    wait('//*[@id="index_perks_list"]/div[4]/div[1]')#等待str元素出現
    driver.find_element_by_xpath(skill[type-1]).click()
    driver.find_element_by_xpath(ornot_gold[isgold]).click()  
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
            if isgold!=0 and isgold!=1:
                print('錯誤輸入')
            else:
                break
        except:
            print('錯誤輸入')
    return [typ,isgold]
def Energy_buy(energy_num):
    driver.get('https://rivalregions.com/')
    wait('//*[@id="header_menu"]/div[6]')
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[6]').click()# 倉庫
    wait('//*[@id="content"]/div[11]/div[3]/span')
    Enegy = int(driver.find_element_by_xpath('//*[@id="content"]/div[11]/div[3]/span').text)# 能量飲料目前數量
    if Enegy <= 600: 
        driver.find_element_by_xpath('//*[@id="content"]/div[11]').click()# 點擊飲料打開購買欄
        wait('//*[@id="storage_market"]/div[2]/div[3]/input')
        num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[3]/input')#抓購買數量框
        num.clear()
        num.send_keys(energy_num)
        driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[4]/div').click()# 輸入並購買   
    else:
        pass
def autominegold(energy_num):
    Energy_buy(energy_num)
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[9]').click()# 生產
    wait('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[2]')
    driver.find_element_by_xpath('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[2]').click()# 自動模式
def minegold(energy_num):
    Energy_buy(energy_num)
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[9]').click()# 生產
    wait('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[1]')
    driver.find_element_by_xpath('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[1]').click()#普通挖金
def halfautowar(weapon_type,weapon_num):
    damage = [75,2000,6000]
    chainfo = getchainfo()
    maxstation = math.floor(math.floor(300/single_costenergy(chainfo['end']))*(1000+50*chainfo['lv'])/damage[int(weapon_type-1)])#最大派兵量={(總能量/單次派兵消耗能量)*該等級攻擊力}/該武器提供的攻擊力
    print(maxstation)
    driver.get('https://rivalregions.com/')
    wait('//*[@id="header_menu"]/div[16]')
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[16]').click() # 戰爭
    wait('//*[@id="content"]/div[4]/div[2]/div')
    driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div').click() # 軍事演習
    wait('//*[@id="send_b_wrap"]/div[4]')
    driver.find_element_by_xpath('//*[@id="send_b_wrap"]/div[4]').click() # 半自動
    driver.find_element_by_xpath('//*[@id="slide_close"]').click() # 返回(X)
    wait('//*[@id="header_menu"]/div[6]')
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[6]').click() # 倉庫
    if weapon_type == 1:
        wait('//*[@id="content"]/div[15]/div[3]/span')
        weapon_now = int(driver.find_element_by_xpath('//*[@id="content"]/div[15]/div[3]/span').text) # 戰機數量
        if weapon_now <= maxstation:
            wait('//*[@id="content"]/div[15]')
            driver.find_element_by_xpath('//*[@id="content"]/div[15]').click() # 點擊戰機打開購買欄
            # 輸入並購買
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input')
            num.clear()
            num.send_keys(weapon_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]').click()
    if weapon_type == 2:
        wait('//*[@id="content"]/div[20]/div[3]/span')
        weapon_now = int(driver.find_element_by_xpath('//*[@id="content"]/div[20]/div[3]/span').text) # 月球戰車數量
        if weapon_now <= maxstation:
            wait('//*[@id="content"]/div[20]')
            driver.find_element_by_xpath('//*[@id="content"]/div[20]').click() # 點擊月球戰車打開購買欄
            # 輸入並購買
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input')
            num.clear()
            num.send_keys(weapon_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]').click()
    if weapon_type == 3:
        wait('//*[@id="content"]/div[19]/div[3]/span')
        weapon_now = int(driver.find_element_by_xpath('//*[@id="content"]/div[19]/div[3]/span').text) # 無人機數量
        if weapon_now <= maxstation:
            wait('//*[@id="content"]/div[19]')
            driver.find_element_by_xpath('//*[@id="content"]/div[19]').click() # 點擊無人機打開購買欄
            # 輸入並購買
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input')
            num.clear()
            num.send_keys(weapon_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]').click()
def main():
    login()
    while True:
        try:
            energy_num = int(input('沒能量飲料時購買數量(請大於600)：'))
            if energy_num>600:
                break
            else:
                print('錯誤!請重新輸入')
        except:
            print('錯誤!請重新輸入')
    while True:
        try:
            weapon_type = int(input('請選擇要買哪種武器1.戰機2.月球戰車3.激光無人機：'))
            if weapon_type!=1 and weapon_type!=2 and weapon_type!=3:
                print('錯誤!請重新輸入')
            else:
                break
        except:
            print('錯誤!請重新輸入')
    while True:
        try:
            weapon_num = int(input('購買數量：'))
            if weapon_num<600:
                print('錯誤!請重新輸入')
            else:
                break
        except:
            print('錯誤!請重新輸入')
    
    halfautowar(weapon_type,weapon_num)
    '''
    while True:
    if iselemexit('//*[@id="header_my_fill_bar_countdown"]'):
        minegold(energy_num)

    '''
        
main()




   


