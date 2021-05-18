#!/usr/bin/env python
# coding: utf-8
import os
import pymysql
from dotenv import load_dotenv
load_dotenv()
import time

from bs4 import BeautifulSoup
import requests
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',"Accept-Language": "en-US,en;q=0.5"}
data = list()

def get_single_page(url):
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content,features="lxml")
    try:
        title = soup.find('div', {'class': 'jobsearch-JobInfoHeader-title-container'}).text
        company = soup.find('div', {'class': 'jobsearch-InlineCompanyRating'}).text
        # location = soup.find_all('div', {'class': 'jobsearch-InlineCompanyRating'})[1].text
        details = soup.find('div', {'id': 'jobDescriptionText'}).text
        t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        print(title,company,'','','',t)
        data.append([title,company,'','','',t,details])
        return data
    except:
        pass
    # data.append([title,company,'','','',t,details])
    return data

def get_searching_page(search_key, start, end):
    urlList = []
    for page in range(start, end+1):
        url = f'https://indeed.com/jobs?q={search_key}&start={page*10}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content,features="lxml")
        companies = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        for company in companies:
            company_id = company.get('data-jk')
            sub_url = f'https://indeed.com/viewjob?jk={company_id}'
            get_single_page(sub_url)
            data = get_single_page(sub_url)
    return data

result = get_searching_page('Data Consultant', 0, 20) #Data Analyst, Data Consultant, 
print('Done!')

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
    back = cursor.executemany("INSERT INTO Job (position,company,location,status,posttime,savetodbtime,details) VALUES(%s,%s,%s,%s,%s,%s,%s)", result) 
    connection.commit()
    print(back)





