from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
from call import *
import numpy as np
import json

with open("data.json","r") as f:
    data = json.load(f)

count = 0
delay = 3
pin = data["pincode"]
website = 'https://www.cowin.gov.in/'

searchbypin = '//*[@id="mat-tab-label-0-1"]/div'
pincodefield = '//*[@id="mat-input-0"]'
login_submit = '//*[@id="mat-tab-content-0-1"]/div/div[1]/div/div/button'
age18plus = '/html/body/app-root/div/app-home/div[3]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div[1]/div/div[1]/label'
databasepath = '/html/body/app-root/div/app-home/div[3]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div[7]'

def construct_df(soup):
    L = soup.findAll(True, {'class':['center-name-title','center-name-text', 'slots-box']})
    
    # obtaining class specific information from soup results
    
    M = []
    for i in L:
        class_names = i.get('class')
        if class_names == ['center-name-title']:
            ADD = i.get_text()
        elif class_names == ['center-name-text']:
            M.append((class_names, ADD + " " + i.get_text()))
        else:
            M.append((class_names, i.get_text()))

    # constructing pandas dataframe
            
    pushelement = None
    data = []
    rownames = []
    for i in M:
        if i[0] == ['center-name-text']:
            rownames.append(i[1])
            if pushelement is not None:
                data.append(pushelement)
            pushelement = []
        else:
            pushelement.append(i[1])
    if pushelement is not None:
        data.append(pushelement)

    # Create the pandas DataFrame
    df = pd.DataFrame(data)
    df.index = rownames
    return df


while(1):

    opts = Options()
    # opts.add_argument('--headless')
    browser = webdriver.Firefox(firefox_options=opts,executable_path='./geckodriver')
    browser.get(website)
    browser.find_element_by_xpath(searchbypin).click()
    
    #clicking on age18 plus button, constructing the dataframe and searching for dose availability

    try:
        pincodefieldobj = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, pincodefield)))
        pincodefieldobj.send_keys(pin)
        
        loginsubmitobj = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, login_submit)))
        loginsubmitobj.click()

        age18p = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, age18plus)))
        age18p.click()
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH,databasepath)))
        soup = BeautifulSoup(myElem.get_attribute('innerHTML'), 'html.parser')
        df = construct_df(soup)

        # call if number of doses for dose 1 is greater than 0
        mask = np.column_stack([df[col].str.contains(r"D1 [1-9][0-9]*") for col in df])

        if mask.any():
            dial()
            count += 1

    except TimeoutException:
        print("Loading took too much time!")
    browser.quit()

    if count == 3:
        break

    time.sleep(600)
