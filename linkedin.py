#pip install selenium
import os
import pymysql
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import random
# from tenacity import retry
from tenacity import *

# proxy
# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
# req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
# proxies = req_proxy.get_proxy_list() #this will create proxy list
# PROXY = proxies[0].get_address()
# webdriver.DesiredCapabilities.CHROME['proxy']={
#     "httpProxy":PROXY,
#     "ftpProxy":PROXY,
#     "sslProxy":PROXY,
    
#     "proxyType":"MANUAL",
    
# }

# set header
"""
Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0
Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0
Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0
https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers/User-Agent
https://developers.whatismybrowser.com/useragents/explore/operating_system_name/macos/5

"""
options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0')
# options.add_argument()
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
driver = webdriver.Chrome(executable_path = '/Users/beckyliu/Data-Engineering-Class-Batch13/students/Becky/individual/chromedriver',options=options) 
# driver = webdriver.Chrome(executable_path = '/Users/beckyliu/Data-Engineering-Class-Batch13/students/Becky/individual/chromedriver') 

def search(position,country):
    driver.get("https://www.linkedin.com/jobs/")
    time.sleep(random.randint(1,3))
    from selenium.webdriver.common.keys import Keys
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.PAGE_DOWN)


    # find the keywords/location search bars:
    search_bars = driver.find_elements_by_class_name('dismissable-input__input')
    search_keywords = search_bars[2]
    search_keywords.send_keys(position)    
    search_location = search_bars[3] 
    time.sleep(5)
    search_location.send_keys(country)
    search_location.send_keys(Keys.RETURN)
    print('searched successfully!')

# #find jobs
# time.sleep(5)
# jobs = driver.find_elements_by_class_name('result-card')
# print('how many jobs on this page: ',len(jobs)) 

# scrolls a single page: 
# Show more
# @retry(wait=wait_fixed(5) + wait_random(0, 5),reraise = True, stop = stop_after_attempt(5))
def getJD():
    #find jobs
    data = []
    time.sleep(5)
    jobs = driver.find_elements_by_class_name('result-card')
    print('================ New Page ================  ')
    print('how many jobs on this page: ',len(jobs)) 
    if len(jobs) == 0:
        time.sleep(random.randint(3,5))
        search('Software Engineer','United States')
        # driver.execute_script('window.scrollTo('+str(random.randint(0,500))+','+ str(random.randint(100,1000))+')') 
        # ele = driver.find_element_by_tag_name('a')
        # webdriver.ActionChains(driver).move_to_element(ele).perform() #selenium.common.exceptions.MoveTargetOutOfBoundsException: Message: move target out of bounds
        # time.sleep(random.randint(3,10))
        raise IOError("Try Again!")
    else:
        jobs = driver.find_elements_by_class_name('result-card')
        for job in jobs:
            driver.execute_script("arguments[0].scrollIntoView();", job)
            job.click()
            time.sleep(random.randint(3,5))
            # get info:
            try:
                [position, company, location,hiringStatus,postTime] = job.text.split('\n')[:5]
                print([position, company, location,hiringStatus,postTime])
                time.sleep(random.randint(1,3))
                showMore = driver.find_elements_by_class_name('show-more-less-html__button')
                showMore[0].click()
                details = driver.find_element_by_class_name("description__text").text
                # print(details)
                t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                data.append([position, company, location,hiringStatus,postTime,t,details])
                print('-------------- Done this Job --------------')
            except:
                continue
    return data
def run():
    start = time.perf_counter() 
    all = list()
    cnt = 0
    search('Software Engineer','United States')
    while cnt <= 5: # 5000 => 165, Finished in 1145.93 second(s)  = 20 min
        cnt += 1
        print(cnt)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(5,10))
        try:
            seeMoreJobs = driver.find_elements_by_class_name('infinite-scroller__show-more-button--visible')
            print("seeMoreJobs")
            # print(seeMoreJobs)
            if len(seeMoreJobs) == 1:
                print('len(seeMoreJobs): ',len(seeMoreJobs))
                time.sleep(5)
                print('=============')
                print(seeMoreJobs[0])
                seeMoreJobs[0].click()
                print('clicked!')            
        except:
            continue
    getJD()
    print('executed getJD()')
    all.extend(getJD())
    return all
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')     
if __name__ == '__main__':
    run()

# Connect mysql
Host = os.getenv("Host")
User = os.getenv("User")
Password = os.getenv("Password")
Path = os.getenv("Path")
connection = pymysql.connect(host=Host,
                             user=User,
                             password=Password,
                             database='JHT',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
with connection:
    cursor = connection.cursor()
    back = cursor.executemany("INSERT INTO Job (position,company,location,status,posttime,savetodbtime,details) VALUES(%s,%s,%s,%s,%s,%s,%s)", run()) 
    connection.commit()
    print(back)
# driver.quit()