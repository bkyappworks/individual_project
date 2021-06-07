import os
import pymysql
from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
# from bs4 import BeautifulSoup
import requests
import random
import urllib.parse as urlparse
from urllib.parse import parse_qs

"""
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
# Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36
# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0
Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1
Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1
ua.safari
"""

options = webdriver.ChromeOptions()
# options.add_argument('user-agent=Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
driver = webdriver.Chrome(executable_path = '/Users/beckyliu/individual_project/chromedriver',options=options) 

# if on EC2
"""
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
options.headless = True
driver = webdriver.Chrome(options=options)

"""

# no scroll one page
def search(position,country):
    driver.get("https://www.linkedin.com/jobs/")
    time.sleep(random.randint(1,3))
    from selenium.webdriver.common.keys import Keys
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.PAGE_DOWN)


    # find the keywords/location search bars:
    search_bars = driver.find_elements_by_class_name('dismissable-input__input')
    print('len(search_bars)',len(search_bars))
    search_keywords = search_bars[2]
    search_keywords.send_keys(position)    
    search_location = search_bars[3] 
    time.sleep(5)
    search_location.send_keys(country)
    search_location.send_keys(Keys.RETURN)
    print('searched successfully!')
# search('Data Engineer','United States')
def getJD():
    #find jobs
    data = []
    time.sleep(5)
    # jobs = driver.find_elements_by_class_name('result-card')
    jobs = driver.find_elements_by_class_name('base-card') #43
    print('================ New Page ================  ')
    print('how many jobs on this page: ',len(jobs)) 
    if len(jobs) == 0:
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        pass
    else:
        # jobs = driver.find_elements_by_class_name('result-card')
        jobs = driver.find_elements_by_class_name('base-card')
        for job in jobs:
            driver.execute_script("arguments[0].scrollIntoView();", job)
            job.click()
            time.sleep(random.randint(3,5))
            # get info:
            try:
                url = driver.current_url
                parsed = urlparse.urlparse(url)
                # print(type(parse_qs(parsed.query)['currentJobId'][0]))
                JobId = parse_qs(parsed.query)['currentJobId'][0]
                t = time.time()
                currentJobId = 'https://www.linkedin.com/jobs/view/'+parse_qs(parsed.query)['currentJobId'][0]
                [position, company, location, hiringStatus, postTime] = job.text.split('\n')[:5]
                print([JobId,position, company, location, hiringStatus, postTime,t])
                time.sleep(random.randint(1,3))
                showMore = driver.find_elements_by_class_name('show-more-less-html__button')
                showMore[0].click()
                details = driver.find_element_by_class_name("description__text").text
                # print(details)
                # t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                data.append([JobId,position, company, location, hiringStatus, postTime,t,currentJobId,details])
                # data.append([position, company, location,hiringStatus,postTime])
                print('-------------- Done this Job --------------')
            except:
                continue
    return data

# getJD()

def saveJobs():
    all = list()
    # search('Software Engineer','United States')
    all.extend(getJD())
    print('--------------  exceute getJD() -------------- ')
    return all

def scroll(position,country):
    start = time.perf_counter() 
    saveall = list()
    search(position,country)
    try:
        # seeMoreJobs = driver.find_elements_by_class_name('infinite-scroller__show-more-button--visible') #original
        seeMoreJobs = driver.find_elements_by_class_name('infinite-scroller__show-more-button')
        print('len(seeMoreJobs): ',len(seeMoreJobs))
        print(seeMoreJobs[0])
        seeMoreJobs[0].click()
        print('clicked!')   
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('clicked and scroll') 
    except:
        # pass
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('keep scroll!')

    saveall.extend(saveJobs())
    # print('saveall[0]: ',saveall[0])
    driver.quit()
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)') 
    return saveall

def saveDB(data):
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
        back = cursor.executemany("INSERT IGNORE INTO job_raw (job_id,position,company,location,hiringstatus,posttime,savetime,url,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", data) 
        # [position, company, location,hiringStatus,postTime,currentJobId,details]
        connection.commit()
        print('Items save to db: ',back)

saveDB(scroll('Data Engineer','United States'))
print('Done!')
