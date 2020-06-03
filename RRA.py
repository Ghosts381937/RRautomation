from selenium import webdriver
from selenium.webdriver.common.keys import Keys #send_keys()
from selenium.webdriver.common.by import By #定位元素
#以下2個套件寫出wait函示
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass#隱藏輸入的密碼
import math
import threading#多執行緒套件
#開啟CHROME
driver_perk = webdriver.Chrome()
driver_gold = webdriver.Chrome()
driver_war = webdriver.Chrome()
driver = [driver_perk,driver_gold,driver_war]
for i in driver:
    i.maximize_window()#最大化視窗
    i.get('https://rivalregions.com/')#開啟RR
def iselemexit(xpath,driver):#檢測該元素是否存在 
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False
def wait(xpath,driver):#當該xpath出現時繼續下個動作,否則等完100秒
    try:
        WebDriverWait(driver,100).until(
            EC.presence_of_element_located((By.XPATH,xpath))
        )
    except :
        driver.refresh()
    time.sleep(1)
def ispremium(driver):#高級會員回傳1,否則回傳0
    #確保連結在遊戲主頁面
    wait('//*[@id="header_money"]/div',driver)
    driver.find_element_by_xpath('//*[@id="header_money"]/div').click()#點擊右上角課金選項
    #獲取是否為高級會員字串
    wait('//*[@id="header_slide_inner"]/div[3]/form[3]/div[3]/div/h1',driver)
    member = driver.find_element_by_xpath('//*[@id="header_slide_inner"]/div[3]/form[3]/div[3]/div/h1').text
    if member[0:2] == '續訂':
        print('高級會員模式.....')
        return 1
    else:
        print('普通會員模式.....')
        return 0
def getchainfo(driver):#get角色資料
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
def howtologin():
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
    return [account,username,password]
def login(account,username,password,driver):#登入
    if account == 1:
        driver.find_element_by_tag_name('div.sa_sn.imp.float_left').click()#點選fb登入
        while True:
            try:
                wait('//*[@id="email"]',driver)
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
                wait('//*[@id="identifierId"]',driver)
                email = driver.find_element_by_xpath('//*[@id="identifierId"]')
                email.send_keys(username)
                email.send_keys(Keys.ENTER)#enter
                break
            except:
                print('錯誤!重新登入中')
        while True:
            try:
                wait('//*[@id="password"]/div[1]/div/div[1]/input',driver)#等待下個頁面跳出
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
                wait('//*[@id="login_submit"]/div/div/input[6]',driver)
                email = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[6]')
                email.send_keys(username)
                pas = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[7]')
                pas.send_keys(password)
                pas.submit()
                break
            except:
                pass
def autoperk(type,isgold,driver):#自動升技
    global acc
    while True:
        skill = ['//*[@id="index_perks_list"]/div[4]/div[1]','//*[@id="index_perks_list"]/div[5]/div[1]','//*[@id="index_perks_list"]/div[6]/div[1]']#技能元素位置
        ornot_gold = ['//*[@id="perk_target_4"]/div[1]/div[1]/div','//*[@id="perk_target_4"]/div[2]/div[1]/div']#是否用金升技能個別位置
        driver.get('https://rivalregions.com/')
        if iselemexit('//*[@id="header_my_avatar"]',driver):
            pass
        else:
            login(acc[0],acc[1],acc[2],driver)  
        wait(skill[type-1],driver)#等待該元素出現
        driver.find_element_by_xpath(skill[type-1]).click()
        time.sleep(1)
        while True:
            if iselemexit('//*[@id="perk_counter_2"]',driver):
                pass
            else:
                if iselemexit('//*[@id="header_my_avatar"]',driver):
                    pass
                else:
                    login(acc[0],acc[1],acc[2],driver)  
                wait(skill[type-1],driver)
                driver.find_element_by_xpath(skill[type-1]).click()
                time.sleep(1)
                driver.find_element_by_xpath(ornot_gold[isgold]).click()
                break
            time.sleep(5)
            driver.refresh()
            wait(skill[type-1],driver)#等待該元素出現
            
        
def howtoperk():#是否用金升技以及升哪個技能
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
def Energy_buy(energy_num,driver):#買能量飲料
    driver.get('https://rivalregions.com/')
    wait('//*[@id="header_menu"]/div[6]',driver)
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[6]').click()# 倉庫
    wait('//*[@id="content"]/div[11]/div[3]/span',driver)
    Enegy = int(driver.find_element_by_xpath('//*[@id="content"]/div[11]/div[3]/span').text)# 能量飲料目前數量
    if Enegy <= 600: 
        driver.find_element_by_xpath('//*[@id="content"]/div[11]').click()# 點擊飲料打開購買欄
        wait('//*[@id="storage_market"]/div[2]/div[3]/input',driver)
        num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[3]/input')#抓購買數量框
        num.clear()
        num.send_keys(energy_num)
        driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[4]/div').click()# 輸入並購買   
    else:
        pass
    driver.get('https://rivalregions.com/')
def weapon_buy(weapon_type,weapon_num,driver):#買武器
    damage = [75,2000,6000]#3種武器分別的傷害
    chainfo = getchainfo(driver)
    maxstation = math.floor(math.floor(300/single_costenergy(chainfo['end']))*(1000+50*chainfo['lv'])/damage[int(weapon_type-1)])#最大派兵量={(總能量/單次派兵消耗能量)*該等級攻擊力}/該武器提供的攻擊力
    driver.get('https://rivalregions.com/')#回首頁
    wait('//*[@id="header_menu"]/div[6]',driver)
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[6]').click() # 倉庫
    if weapon_type == 1:
        wait('//*[@id="content"]/div[15]/div[3]/span',driver)
        weapon_now = int(driver.find_element_by_xpath('//*[@id="content"]/div[15]/div[3]/span').text) # 戰機數量
        if weapon_now <= maxstation:
            wait('//*[@id="content"]/div[15]',driver)
            driver.find_element_by_xpath('//*[@id="content"]/div[15]').click() # 點擊戰機打開購買欄
            # 輸入並購買
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input')
            num.clear()
            num.send_keys(weapon_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]').click()
    elif weapon_type == 2:
        wait('//*[@id="content"]/div[20]/div[3]/span',driver)
        weapon_now = int(driver.find_element_by_xpath('//*[@id="content"]/div[20]/div[3]/span').text) # 月球戰車數量
        if weapon_now <= maxstation:
            wait('//*[@id="content"]/div[20]',driver)
            driver.find_element_by_xpath('//*[@id="content"]/div[20]').click() # 點擊月球戰車打開購買欄
            # 輸入並購買
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input')
            num.clear()
            num.send_keys(weapon_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]').click()
    elif weapon_type == 3:
        wait('//*[@id="content"]/div[19]/div[3]/span',driver)
        weapon_now = int(driver.find_element_by_xpath('//*[@id="content"]/div[19]/div[3]/span').text) # 無人機數量
        if weapon_now <= maxstation:
            wait('//*[@id="content"]/div[19]',driver)
            driver.find_element_by_xpath('//*[@id="content"]/div[19]').click() # 點擊無人機打開購買欄
            # 輸入並購買
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input')
            num.clear()
            num.send_keys(weapon_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]').click()
    driver.get('https://rivalregions.com/')
def autominegold(energy_num,driver):#自動挖金
    Energy_buy(energy_num,driver)
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[9]').click()# 生產
    wait('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[2]',driver)
    driver.find_element_by_xpath('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[2]').click()# 自動模式
def minegold(energy_num,driver):#手動挖金
    Energy_buy(energy_num,driver)
    if int(driver.find_element_by_xpath('//*[@id="s_index"]').text)<200:
        driver.find_element_by_xpath('//*[@id="header_my_fill_bar"]').click()
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[9]').click()# 生產
    wait('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[1]',driver)
    driver.find_element_by_xpath('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[1]').click()#普通挖金
def halfautowar(weapon_type,weapon_num,driver):#半自動演習
    weapon_buy(weapon_type,weapon_num,driver)
    wait('//*[@id="header_menu"]/div[16]',driver)
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[16]').click() # 戰爭
    wait('//*[@id="content"]/div[4]/div[2]/div',driver)
    driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div').click() # 軍事演習
    wait('//*[@id="send_b_wrap"]/div[4]',driver)
    driver.find_element_by_xpath('//*[@id="send_b_wrap"]/div[4]').click() # 半自動
def manualwar(weapon_type,weapon_num,driver):#手動演習
    weapon_buy(weapon_type,weapon_num,driver)
    wait('//*[@id="header_menu"]/div[16]',driver)
    driver.find_element_by_xpath('//*[@id="header_menu"]/div[16]').click() # 戰爭
    wait('//*[@id="content"]/div[4]/div[2]/div',driver)
    driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div').click() # 軍事演習
    wait('//*[@id="send_b_wrap"]/div[1]',driver)
    driver.find_element_by_xpath('//*[@id="send_b_wrap"]/div[1]').click()#派兵
def howtobuy_energy():#沒能量飲料時購買數量
    while True:
        try:
            energy_num = int(input('沒能量飲料時購買數量(請大於600)：'))
            if energy_num>600:
                return energy_num
            else:
                print('錯誤!請重新輸入')
        except:
            print('錯誤!請重新輸入')
def howtobuy_weapon():#購買武器的種類及數量
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
                return [weapon_type,weapon_num]
        except:
            print('錯誤!請重新輸入')
def thread_create(arg1,arg2,arg3,mode):#創建執行緒
    goldfunc = [minegold,autominegold]
    warfunc = [manualwar,halfautowar]
    t1 = threading.Thread(target = autoperk,args = (arg1[0],arg1[1],driver_perk))
    t2 = threading.Thread(target = goldfunc[mode],args = (arg2,driver_gold))
    t3 = threading.Thread(target = warfunc[mode],args = (arg3[0],arg3[1],driver_war))
    return [t1,t2,t3]
def main():
    global acc
    acc = howtologin()
    for i in driver:
        login(acc[0],acc[1],acc[2],i)
    mode = ispremium(driver_perk)
    print('升級技能:')
    perk = howtoperk()
    print('挖金礦:')
    energy_num = howtobuy_energy()
    print('戰爭:')
    war = howtobuy_weapon()
    thread = thread_create(perk,energy_num,war,mode)
    thread[0].start()
main()




   


