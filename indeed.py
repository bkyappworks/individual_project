#!/usr/bin/env python
# coding: utf-8
import sqlalchemy
from sqlalchemy import create_engine
import os
import pymysql
import re, time
import os
import pymysql
from dotenv import load_dotenv
load_dotenv()
import time

from bs4 import BeautifulSoup
import requests

"""
Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0
Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1
Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1
"""

headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',"Accept-Language": "en-US,en;q=0.5"}

def get_single_page(url):
    # url = 'https://www.indeed.com/viewjob?jk=6fe8eebdc5bcf567'
    data_list = list()
    r = requests.get(url) #r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content,features="lxml")

    job_id = re.findall(r'jk=.*',url)[0][3:]
    position = soup.find('div', {'class': 'jobsearch-JobInfoHeader-title-container'}).text
    cr = soup.find('div', {'class': 'jobsearch-InlineCompanyRating'}).text
    company = re.findall(r'[A-Z][a-z]*',cr)
    company = ' '.join(company)
    reviews = re.findall(r'[1-9]',cr)
    reviews = ''.join(reviews)
    loc = soup.find('div', {'class': 'icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle'}).text
    try: 
        location = re.findall(r'reviews.*',loc)[0][7:]
    except: 
        location = ''
    hiringStatus = ''
    postTime = soup.find('div', {'class': 'jobsearch-JobMetadataFooter'}).text
    postTime = re.findall(r'[0-9].*s',postTime)
    if len(postTime) >= 1:
        postTime = ''.join(postTime)
        # print(postTime)
    else:
        postTime = 'Today'
        # print(postTime)
    t = time.time()
    url = url
    details = soup.find('div', {'id': 'jobDescriptionText'}).text
    data_list = [job_id, position, company, location, hiringStatus, postTime,t,url,details]
    print([job_id, position, company, location, hiringStatus, postTime,t,url])
    return data_list

def get_searching_page(search_key, start, end):
    final_data = list()
    for page in range(start, end+1):
        url = f'https://indeed.com/jobs?q={search_key}&start={page*10}'
        # url = f'https://indeed.com/jobs?q={search_key}&start={page*10}'
        print(url) # https://indeed.com/jobs?q=Data Engineer&start=10
        r = requests.get(url)
        soup = BeautifulSoup(r.content,features="lxml")
        companies = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        for company in companies:
            company_id = company.get('data-jk')
            sub_url = f'https://indeed.com/viewjob?jk={company_id}'
            # get_single_page(sub_url)
            final_data.append(get_single_page(sub_url)) 
    print(len(final_data))
    return final_data

def saveDB(data):
    Host = os.getenv("Host")
    User = os.getenv("User")
    Password = os.getenv("Password")
    Path = os.getenv("Path")
    connection_string = 'mysql+pymysql://'+User+':'+Password+'@'+Host+':3306/JHT'
    engine = create_engine(connection_string,echo = True)
    connection = engine.raw_connection()
    cursor = connection.cursor()
    # data = [['2589941272', 'Data Engineer', 'Coca-Cola Beverages Florida', 'Orlando, FL', 'Be an early applicant', '3 hours ago', 1623229806.096464, 'https://www.linkedin.com/jobs/view/2589941272', "Orlando, FL, USA\nTampa, FL, USA Req #6759 Friday, June 4, 2021 Coca-Cola Beverages Florida, LLC (Coke Florida) is a family-owned independent Coca-Cola bottler that is the third largest privately-held and the sixth largest independent Coca-Cola bottler in the United States. Coke Florida's exclusive territory covers over 18 million consumers across 47 Florida counties, and includes the major metropolitan markets of Jacksonville, Miami, Orlando and Tampa. Coke Florida sells, markets, manufactures and distributes over 600 products of The Coca-Cola Company and other partner companies including Monster Beverage Corporation and BODYARMOR. In 2017, Coke Florida generated over $1.2 billion in revenue and the company currently has approximately 4,800 employees. As one of the first US greenfield independent Coca-Cola bottlers in nearly sixty years, Coke Florida is at an exciting stage in its transformational journey to become a leading-edge beverage company, the best bottler in the Coca-Cola System, and one of the best companies to work for in Florida. The Data Engineer is a key member of the Coke Florida Information Governance Organization responsible for supporting, managing, and optimizing data pipelines to support business/data analysts, data scientists or any persona that needs curated data for data and analytics use cases across the enterprise. Role Responsibilities\nBuild platforms and pipeline to enables teams to clearly and clearly analyze data, build models and drive decisions\nCreate, maintain, and optimize data pipelines within the Coke Florida system\nAssist with driving automation through effective metadata management, assist with renovating data management infrastructure to drive automation in data integration and management\nBecome a Subject Matter Expert (SME) on data within Coke Florida, how it flows through which systems and how it can interact with other systems\nParticipate in ensuring complete and governance during data use\nWork with various APIs to integrate with internal data models\nRole Requirements\nBachelor's or Master's degree in computer science, statistics, data management or equivalent work experience\n6+ years work experience in data management disciplines including data integration, modeling, optimization and data quality, and/or other areas directly to data engineering responsibilities and tasks\n3+ years experience working in cross-functional teams and collaborating with key stakeholders\nExperience with ETL, data replication, API design is highly desired\nExperience with SAP Snowflake highly desired\nExperience with cloud tools, such as Azure\nPrevious experience with data management architectures such as Data Warehouse, Data Lake, Data Hub and the supporting processes like Data Integration, Governance Metadata Management\nThis job description is not an exhaustive list of all functions that the employee may be required to perform, and the employee may be required to perform additional functions. Coke Florida reserves the right to revise the job description at any time. Employment with Coke Florida is at-will. The employee must be able to perform the essential functions of the position satisfactorily and, if requested, reasonable accommodations may be made to enable employees with disabilities to perform essential functions of their job, absent undue hardship.\n\nCoca-Cola Beverages Florida is an Equal Opportunity Employer and does not discriminate against any employee or applicant for employment because of race, color, sex, age, national origin, religion, sexual orientation, gender identity and/or expression, status as a veteran, and basis of disability or any other federal, state or local protected class.\n\nOther Details\nJob Family Technology/Transformation\nJob Function Information Governance\nPay Type Salary\nApply Now\nOrlando, FL, USA\nTampa, FL, USA\nShow less"]]
    back = cursor.executemany("INSERT IGNORE INTO job_raw (job_id,position,company,location,hiringstatus,posttime,savetime,url,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", data) 
    connection.commit()
    print('Items save to db: ',back)
    print('Done!')

saveDB(get_searching_page('Data Engineer', 0, 1))





