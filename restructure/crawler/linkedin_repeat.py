import sqlalchemy
from sqlalchemy import create_engine
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
                # print([JobId,position, company, location, hiringStatus, postTime,t,currentJobId,details])
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
    # connection = pymysql.connect(host=Host,
    #                             user=User,
    #                             password=Password,
    #                             database='JHT',
    #                             charset='utf8mb4',
    #                             cursorclass=pymysql.cursors.DictCursor)
    connection_string = 'mysql+pymysql://'+User+':'+Password+'@'+Host+':3306/JHT'
    engine = create_engine(connection_string,echo = True)
    connection = engine.raw_connection()
    # cursor = connection.cursor()
    # print(cursor)
    # with connection:
    cursor = connection.cursor()
    # data = [['2589941272', 'Data Engineer', 'Coca-Cola Beverages Florida', 'Orlando, FL', 'Be an early applicant', '3 hours ago', 1623229806.096464, 'https://www.linkedin.com/jobs/view/2589941272', "Orlando, FL, USA\nTampa, FL, USA Req #6759 Friday, June 4, 2021 Coca-Cola Beverages Florida, LLC (Coke Florida) is a family-owned independent Coca-Cola bottler that is the third largest privately-held and the sixth largest independent Coca-Cola bottler in the United States. Coke Florida's exclusive territory covers over 18 million consumers across 47 Florida counties, and includes the major metropolitan markets of Jacksonville, Miami, Orlando and Tampa. Coke Florida sells, markets, manufactures and distributes over 600 products of The Coca-Cola Company and other partner companies including Monster Beverage Corporation and BODYARMOR. In 2017, Coke Florida generated over $1.2 billion in revenue and the company currently has approximately 4,800 employees. As one of the first US greenfield independent Coca-Cola bottlers in nearly sixty years, Coke Florida is at an exciting stage in its transformational journey to become a leading-edge beverage company, the best bottler in the Coca-Cola System, and one of the best companies to work for in Florida. The Data Engineer is a key member of the Coke Florida Information Governance Organization responsible for supporting, managing, and optimizing data pipelines to support business/data analysts, data scientists or any persona that needs curated data for data and analytics use cases across the enterprise. Role Responsibilities\nBuild platforms and pipeline to enables teams to clearly and clearly analyze data, build models and drive decisions\nCreate, maintain, and optimize data pipelines within the Coke Florida system\nAssist with driving automation through effective metadata management, assist with renovating data management infrastructure to drive automation in data integration and management\nBecome a Subject Matter Expert (SME) on data within Coke Florida, how it flows through which systems and how it can interact with other systems\nParticipate in ensuring complete and governance during data use\nWork with various APIs to integrate with internal data models\nRole Requirements\nBachelor's or Master's degree in computer science, statistics, data management or equivalent work experience\n6+ years work experience in data management disciplines including data integration, modeling, optimization and data quality, and/or other areas directly to data engineering responsibilities and tasks\n3+ years experience working in cross-functional teams and collaborating with key stakeholders\nExperience with ETL, data replication, API design is highly desired\nExperience with SAP Snowflake highly desired\nExperience with cloud tools, such as Azure\nPrevious experience with data management architectures such as Data Warehouse, Data Lake, Data Hub and the supporting processes like Data Integration, Governance Metadata Management\nThis job description is not an exhaustive list of all functions that the employee may be required to perform, and the employee may be required to perform additional functions. Coke Florida reserves the right to revise the job description at any time. Employment with Coke Florida is at-will. The employee must be able to perform the essential functions of the position satisfactorily and, if requested, reasonable accommodations may be made to enable employees with disabilities to perform essential functions of their job, absent undue hardship.\n\nCoca-Cola Beverages Florida is an Equal Opportunity Employer and does not discriminate against any employee or applicant for employment because of race, color, sex, age, national origin, religion, sexual orientation, gender identity and/or expression, status as a veteran, and basis of disability or any other federal, state or local protected class.\n\nOther Details\nJob Family Technology/Transformation\nJob Function Information Governance\nPay Type Salary\nApply Now\nOrlando, FL, USA\nTampa, FL, USA\nShow less"]]
    back = cursor.executemany("INSERT IGNORE INTO job_raw (job_id,position,company,location,hiringstatus,posttime,savetime,url,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", data) 
    connection.commit()
    print('Items save to db: ',back)
saveDB(scroll('Fronend Engineer','United States')) # Software Engineer, Data Scientist, Fronend Engineer, Backend Engineer, Data Analyst, Data Engineer
print('Done!')
