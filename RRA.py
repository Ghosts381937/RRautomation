from selenium import webdriver
from selenium.webdriver.common.keys import Keys #send_keys()
from selenium.webdriver.common.by import By #定位元素
#以下2個套件寫出wait函示
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options#給定瀏覽器設定值
import time #用於time.sleep()
import math 
import threading#多執行緒套件
from queue import Queue #處理執行緒回傳值
from retrying import retry #function跳出錯誤時重新執行
from getpass import getpass 
global switch #控制while迴圈的變數(搭配後方thread_kill)
switch = 1
chrome_options = Options()
chrome_options.add_argument('window-size=1280,720') 
chrome_options.add_argument('log-level=3') #調高回傳log會顯示的等級
chrome_options.add_argument('blink-settings=imagesEnabled=false')#關閉圖片載入
chrome_options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'")
path = 'chromedriver.exe'
#開啟CHROME
def driver_create(q):
    driver = webdriver.Chrome(options=chrome_options,executable_path=path) #開始瀏覽器
    driver.get('https://rivalregions.com/')#開啟RR
    q.put(driver) #從執行緒拿回傳值
t_tmp = list()
q = Queue() #queue型態
#開啟3個driver_create執行緒並放入t_tmp
for i in range(3):
    t0 = threading.Thread(target=driver_create,args=(q,))
    t0.start()
    t_tmp.append(t0)
#依序停止t_tmp裡的3個執行緒
for thread in t_tmp:
    thread.join()
#從q依序拿創建好的瀏覽器出來
driver_perk = q.get()
driver_gold = q.get()
driver_war = q.get()
print('成功開啟瀏覽器')
driver = [driver_perk,driver_gold,driver_war]
def iselemexit(xpath,driver):#檢測該元素是否存在 
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False
def click(elem): #點擊該元素(6次點擊失敗後跳出)
    global switch
    count=0
    while switch:
        if count>5:
            break
        try:
            elem.click()
            break
        except:
            count=count+1
            time.sleep(1)
def wait(xpath,driver):#當該xpath出現時繼續下個動作,否則等完10秒後refresh(最多等30秒)
    global switch
    count = 0
    while switch:
        if count>2:
            break
        try:
            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH,xpath))
            )
            time.sleep(2)
            break
        except:
            count = count + 1
            driver.refresh()
def ispremium(driver):#高級會員回傳1,否則回傳0
    #確保連結在遊戲主頁面
    wait('//*[@id="header_money"]/div',driver)
    click(driver.find_element_by_xpath('//*[@id="header_money"]/div'))#點擊右上角課金選項
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
    global switch
    while switch:
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
    password = getpass('請輸入密碼:')
    return [account,username,password]
def login(account,username,password,driver):#登入
    global switch
    if account == 1:
        click(driver.find_element_by_tag_name('div.sa_sn.imp.float_left'))#點選fb登入
        while switch:
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
        click(driver.find_element_by_tag_name('div.sa_sn.float_left.imp.gogo'))
        while switch:
            try:
                wait('//*[@id="identifierId"]',driver)
                email = driver.find_element_by_xpath('//*[@id="identifierId"]')
                email.send_keys(username)
                email.send_keys(Keys.ENTER)#enter
                break
            except:
                print('錯誤!重新登入中')
        while switch:
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
        click(driver.find_element_by_xpath('//*[@id="sa_add2"]/div[2]/a[3]/div'))
        while switch:
            try:
                wait('//*[@id="login_submit"]/div/div/input[6]',driver)
                email = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[6]')
                email.send_keys(username)
                pas = driver.find_element_by_xpath('//*[@id="login_submit"]/div/div/input[7]')
                pas.send_keys(password)
                pas.submit()
                break
            except:
                print('錯誤!重新登入中')
def relogin(acc_type,driver):
    if iselemexit('//*[@id="header_my_avatar"]',driver):#左上頭貼再登入狀態時才會出現
        pass
    else:
        print('重新登入中')
        driver.get('https://rivalregions.com/')
        driver.refresh()
        wait('div.sa_sn.float_left.imp.gogo',driver)
        click(driver.find_element_by_tag_name('div.sa_sn.float_left.imp.gogo'))
        wait('//*[@id="header_my_avatar"]',driver)
@retry()#function跳出錯誤時重新執行
def autoperk(type,isgold,driver):#自動升技
    global switch
    global acc
    driver.get('https://rivalregions.com/')
    skill = ['//*[@id="index_perks_list"]/div[4]/div[1]','//*[@id="index_perks_list"]/div[5]/div[1]','//*[@id="index_perks_list"]/div[6]/div[1]']#技能元素位置
    ornot_gold = ['//*[@id="perk_target_4"]/div[1]/div[1]/div','//*[@id="perk_target_4"]/div[2]/div[1]/div']#是否用金升技能個別位置
    while switch:
        wait(skill[type-1],driver) #等待所選技能欄位出現
        #若頁面上有倒數計時(目前在升級中)
        if iselemexit('//*[@id="perk_counter_2"]',driver):
            time.sleep(10)
            driver.refresh()#頁面重整
        else:
            relogin(acc[0],driver)
            click(driver.find_element_by_xpath(skill[type-1]))#點擊該技能
            time.sleep(1)
            click(driver.find_element_by_xpath(ornot_gold[isgold]))#點擊升級
def howtoperk():#是否用金升技以及升哪個技能
    global switch
    while switch:
        try:
            typ = int(input('請輸入欲升級的技能(1.STR 2.EDU 3.END):'))
            if typ!=1 and typ!=2 and typ!=3:
                print('錯誤輸入')
            else:
                break
        except:
            print('錯誤輸入')
    while switch:
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
    global acc
    relogin(acc[0],driver)
    wait('//*[@id="header_menu"]/div[6]',driver)
    click(driver.find_element_by_xpath('//*[@id="header_menu"]/div[6]'))# 倉庫
    wait('//*[@id="content"]/div[11]/div[3]/span',driver)
    Enegy = int(driver.find_element_by_xpath('//*[@id="content"]/div[11]/div[3]/span').text.replace('.',''))# 能量飲料目前數量
    if Enegy <= 600: 
        click(driver.find_element_by_xpath('//*[@id="content"]/div[11]'))# 點擊飲料打開購買欄
        wait('//*[@id="storage_market"]/div[2]/div[3]/input',driver)
        num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[3]/input')#抓購買數量框
        num.clear()
        num.send_keys(energy_num)
        click(driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[4]/div'))# 輸入並購買   
    else:
        pass
def weapon_buy(weapon_type,weapon_num,driver):#買武器
    global maxstation
    global chainfo
    damage = [75,2000,6000]#3種武器分別的傷害
    maxstation = math.floor(math.floor(300/single_costenergy(chainfo['end']))*(1000+50*chainfo['lv'])/damage[int(weapon_type-1)])#最大派兵量={(總能量/單次派兵消耗能量)*該等級攻擊力}/該武器提供的攻擊力
    relogin(acc[0],driver)
    driver.get('https://rivalregions.com/#storage')
    driver.refresh()
    if weapon_type == 1:
        wait('//*[@id="content"]/div[15]/div[3]/span',driver)
        weapon_now = int(driver.find_element_by_xpath('//*[@id="content"]/div[15]/div[3]/span').text.replace('.','')) # 戰機數量
        if weapon_now <= maxstation:
            wait('//*[@id="content"]/div[15]',driver)
            click(driver.find_element_by_xpath('//*[@id="content"]/div[15]')) # 點擊戰機打開購買欄
            wait('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input',driver)
            # 輸入並購買
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input')
            num.clear()
            num.send_keys(weapon_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]').click()
    elif weapon_type == 2:
        wait('//*[@id="content"]/div[20]/div[3]/span',driver)
        weapon_now = int(driver.find_element_by_xpath('//*[@id="content"]/div[20]/div[3]/span').text.replace('.','')) # 月球戰車數量
        if weapon_now <= maxstation:
            wait('//*[@id="content"]/div[20]',driver)
            click(driver.find_element_by_xpath('//*[@id="content"]/div[20]')) # 點擊月球戰車打開購買欄
            wait('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input',driver)
            # 輸入並購買
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input')
            num.clear()
            num.send_keys(weapon_num)
            driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]').click()
    elif weapon_type == 3:
        wait('//*[@id="content"]/div[19]/div[3]/span',driver)
        weapon_now = int(driver.find_element_by_xpath('//*[@id="content"]/div[19]/div[3]/span').text.replace('.','')) # 無人機數量
        if weapon_now <= maxstation:
            wait('//*[@id="content"]/div[19]',driver)
            click(driver.find_element_by_xpath('//*[@id="content"]/div[19]')) # 點擊無人機打開購買欄
            wait('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input',driver)
            # 輸入並購買
            num = driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[5]/input')
            num.clear()
            num.send_keys(weapon_num)
            click(driver.find_element_by_xpath('//*[@id="storage_market"]/div[2]/div[1]/div[6]/div[1]'))
@retry()
def autominegold(energy_num,driver):#自動挖金
    global switch
    while switch:
        Energy_buy(energy_num,driver)
        wait('//*[@id="header_menu"]/div[9]',driver)
        click(driver.find_element_by_xpath('//*[@id="header_menu"]/div[9]'))#生產
        wait('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[2]',driver)
        if driver.find_element_by_xpath('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[2]').text == '自動模式':
            click(driver.find_element_by_xpath('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[2]'))#自動模式
        time.sleep(60)
@retry()
def minegold(energy_num,driver):#手動挖金
    global switch
    while switch:
        Energy_buy(energy_num,driver)
        wait('//*[@id="s_index"]',driver)
        if int(driver.find_element_by_xpath('//*[@id="s_index"]').text)<200 and iselemexit('//*[@id="header_my_fill_bar"]',driver):
            click(driver.find_element_by_xpath('//*[@id="header_my_fill_bar"]'))
        wait('//*[@id="header_menu"]/div[9]',driver)
        click(driver.find_element_by_xpath('//*[@id="header_menu"]/div[9]'))# 生產
        wait('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[1]',driver)
        click(driver.find_element_by_xpath('//*[@id="content"]/div[6]/div[2]/div[2]/div[3]/div[1]'))#普通挖金
        time.sleep(60)
        
@retry()
def halfautowar(weapon_type,weapon_num,driver):#半自動演習
    global switch
    global maxstation
    while switch:
        weapon_buy(weapon_type,weapon_num,driver)
        wait('//*[@id="header_menu"]/div[16]',driver)
        click(driver.find_element_by_xpath('//*[@id="header_menu"]/div[16]')) # 戰爭
        wait('//*[@id="content"]/div[4]/div[2]/div',driver)
        click(driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div')) #軍事演習
        wait('//*[@id="header_slide_inner"]/div[2]/h1/div[2]',driver)
        if iselemexit('//*[@id="send_b_wrap"]/div[4]',driver):
            inputbox = driver.find_element_by_xpath('//*[@id="header_slide_inner"]/div[4]/div[2]/div[3]/input')
            inputbox.clear()
            inputbox.send_keys(maxstation)
            click(driver.find_element_by_xpath('//*[@id="send_b_wrap"]/div[4]')) # 半自動
        time.sleep(60)
@retry()
def manualwar(weapon_type,weapon_num,driver):#手動演習
    global switch
    global maxstation
    while switch:
        weapon_buy(weapon_type,weapon_num,driver)
        wait('//*[@id="header_menu"]/div[16]',driver)
        click(driver.find_element_by_xpath('//*[@id="header_menu"]/div[16]')) # 戰爭
        wait('//*[@id="content"]/div[4]/div[2]/div',driver)
        click(driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/div')) # 軍事演習
        wait('//*[@id="header_slide_inner"]/div[2]/h1/div[2]',driver)
        if iselemexit('//*[@id="send_b_wrap"]/div[1]',driver):
                inputbox = driver.find_element_by_xpath('//*[@id="header_slide_inner"]/div[4]/div[2]/div[3]/input')
                inputbox.clear()
                inputbox.send_keys(maxstation)
                click(driver.find_element_by_xpath('//*[@id="send_b_wrap"]/div[1]'))#派兵
        time.sleep(60)
def howtobuy_energy():#沒能量飲料時購買數量
    global switch
    while switch:
        try:
            energy_num = int(input('沒能量飲料時購買數量(請大於600)：'))
            if energy_num>600:
                return energy_num
            else:
                print('錯誤!請重新輸入')
        except:
            print('錯誤!請重新輸入')
def howtobuy_weapon():#購買武器的種類及數量
    global switch
    while switch:
        try:
            weapon_type = int(input('請選擇要買哪種武器1.戰機2.月球戰車3.激光無人機：'))
            if weapon_type!=1 and weapon_type!=2 and weapon_type!=3:
                print('錯誤!請重新輸入')
            else:
                break
        except:
            print('錯誤!請重新輸入')
    while switch:
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
    t4 = threading.Thread(target = thread_kill)
    return [t1,t2,t3,t4]
def thread_kill():
    global switch
    global thread
    while switch:
        try:
            switch = int(input('輸入0關閉程式:'))
            if switch == 0:
                print('程式關閉中.....')
                thread[0].join()
                thread[1].join()
                thread[2].join()
                for browser in driver:
                    browser.close()
                print('成功關閉程式.....')
            else:
                print('錯誤輸入!')
        except:
            print('錯誤輸入!')
def main():
    global acc #存登入資訊
    global switch
    global thread
    global chainfo
    acc = howtologin()
    t_tmp = list()
    for i in driver:
        t = threading.Thread(target=login,args=(acc[0],acc[1],acc[2],i))
        t.start()
        t_tmp.append(t)
    for t in t_tmp:
        t.join()
    mode = ispremium(driver_perk)
    chainfo = getchainfo(driver_war)
    print('升級技能:')
    perk = howtoperk()
    print('挖金礦:')
    energy_num = howtobuy_energy()
    print('戰爭:')
    war = howtobuy_weapon()
    thread = thread_create(perk,energy_num,war,mode)
    thread[0].start()
    thread[1].start()
    thread[2].start()
    thread[3].start()
    thread[3].join()
main()