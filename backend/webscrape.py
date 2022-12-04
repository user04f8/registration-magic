
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests 
import time

def browser_function():
    driver_path = '/usr/local/bin/chromedriver'
    #keeps browser open
    chr_options = Options()
    chr_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(driver_path, options=chr_options)
    #redirects to bu login page, enter login, will redirect to the list of courses to register
    #first available CAS course, CAS AA 385 A1
    driver.get('https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1670173994?College=CAS&Dept=AA&Course=310&Section=A1&ModuleName=reg%2Fadd%2Fbrowse_schedule.pl&AddPreregInd=&AddPlannerInd=&ViewSem=Spring+2023&KeySem=20234&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList=')
    time.sleep(30)
    return driver

def web_scrape():
   driver = browser_function()
   input = driver.find_element('name','SelectIt')
   print(input.get_attribute('value'))



web_scrape()

# driver.get("https://...)
# driver.implicitly_wait(6)
# driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(userid)
# driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
# driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()
# driver.get("https://www.linkedin.com/search/results/all/? 
# keywords=director%20supply%20chain&origin=GLOBAL_SEARCH_HEADER&page=1")