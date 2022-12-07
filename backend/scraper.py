from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
import xlsxwriter
import time
import secret

def browser_login() -> webdriver:

    #instantiating web driver 
    #keeps web browser open while scraping
    chrome_options = Options()
    path = Service('/usr/local/bin/chromedriver')
    chrome_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(service=path, options=chrome_options)

    #stored in seperate .py file with my login credentials 
    username = secret.username
    password = secret.password

    login_url = 'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1670304546?College=CAS&Dept=AA&Course=310&Section=A1&ModuleName=reg%2Fadd%2Fbrowse_schedule.pl&AddPreregInd=&AddPlannerInd=Y&ViewSem=Spring+2023&KeySem=20234&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList='
    #get the url, and automatically login with credentials
    driver.get(login_url)
    driver.find_element(By.NAME, 'j_username').send_keys(username)
    driver.find_element(By.NAME, 'j_password').send_keys(password)
    time.sleep(1)

    #clicks the continue button after logging in
    driver.find_element(By.NAME, '_eventId_proceed').click()
    time.sleep(1)

    #switches iframe in order to locate the button "call me" in for duo 2fa
    driver.switch_to.frame('duo_iframe')
    driver.find_element(By.XPATH,'//*[@id="auth_methods"]/fieldset/div[1]/button').click()
    time.sleep(1)

    time.sleep(10)
    return driver

#Function that was intended to break down the href link into the components of the course information
    # def course_identifiers(course_url: str) -> list[str]:
    #     index_first = course_url.find('ClassCd=') + 8
    #     index_last = course_url.find('&TopicCd=')
    #     course_url = course_url[index_first:index_last]

    #     college = course_url[0:3]
    #     dept = course_url[3:5]
    #     course_num = course_url[5:8]
    #     section = course_url[11:]

    #     course_info_list = [college, dept, course_num, section]
    #     return course_info_list


def web_scrape():
    #instantiating login and driver element returned from browser_login
    driver = browser_login()
    #creating file
    filename = "Course_Info.xlsx"
    outWorkbook = xlsxwriter.Workbook(filename)
    outSheet = outWorkbook.add_worksheet()
    outSheet.write("A1", "SelectIt")
    outSheet.write("B1", "College")
    #row counter n, variable used to increment each row in sheet
    #int counter i, increments array index
    x,n,i = 1,1,0


    colleges = ["CAS","BUA","CDS","CFS","CGS","COM","ENG","EOP","FRA","GMS","GRS","HUB","KHC","LAW","MED","MET","OTP","PDP","QST","SAR","SDM","SED","SHA","SPH","SSW","STH","XAS","XRG"]
    #runs until we reach the last page of the student link
    while True:

    #Attempted to get href link for each course, but could not filter out links that are for courses that ARE available
    #the href link contains ClassCd with all course information
     #course_urls = set(driver.find_elements(By.TAG_NAME, 'a'))
        # for course_url in course_urls:
        #     c_info = course_url.get_attribute('href')
        #     c_info_list = course_identifiers(c_info)
        #     for count, info in enumerate(c_info_list):
        #         outSheet.write(x, count, info)
        #     x += 1
        #     c_info_list = []

    #clicks on nextpage, else throws exception 
        try:
            checkboxes = driver.find_elements(By.XPATH,"//input[@type= 'checkbox']")
            #loops through all checkboxes for each page, gets selectit and writes to the file
            for checkbox in checkboxes:
                select_it = checkbox.get_attribute('value')
                outSheet.write(n, 0, select_it)
                outSheet.write(n, 1, colleges[i])
                n += 1
            
            next_page = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/center[2]/table/tbody/tr/td[2]/input')))
            next_page.click()
            time.sleep(1)
        #exception handles when we reach the end page of all courses for a given college, chooses next college in list, continues search
        except UnexpectedAlertPresentException:
            time.sleep(3)
            if(i < len(colleges)-1):
                i += 1
            else:
                break
            driver.find_element(By.NAME, 'College').send_keys(colleges[i])
            time.sleep(1)
            next_page.click()
            continue
        #exception handles when we reach a page where we cannot access information, bu error says "No classes found for specified search criteria"
        #goes back a page and enters another college from the colleges list, continues search
        except TimeoutException:
            time.sleep(3)
            driver.execute_script("window.history.go(-1)")
            time.sleep(1)
            if(i < len(colleges)-1):
                i += 1
            else:
                break
            driver.find_element(By.NAME, 'College').send_keys(colleges[i])
            next_page = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/center[2]/table/tbody/tr/td[2]/input')))
            next_page.click()
            continue
    
    #close file, quit the driver
    print('web scraping done!')
    outWorkbook.close()
    driver.quit()


#main
web_scrape()

