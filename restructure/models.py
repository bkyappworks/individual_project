from pymysql import connect
from collections import OrderedDict
import operator
import requests
import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy import create_engine
import re, time, pymysql.cursors, pymysql
import os
from dotenv import load_dotenv
load_dotenv()

Host = os.getenv("Host")
User = os.getenv("User")
Password = os.getenv("Password")
Path = os.getenv("Path")

# engine = create_engine('mysql+pymysql://'+User+':'+Password+'@localhost/JHT',echo = True)
connection_string = 'mysql+pymysql://'+User+':'+Password+'@'+Host+':3306/JHT'
engine = create_engine(connection_string,pool_recycle=3600)
connection = engine.raw_connection()
cursor = connection.cursor()
# connection.ping(reconnect=True) 

import time
tod = time.time()

# jobinfo
def jobinfo(title):
    cursor = connection.cursor()
    cursor.execute("select job_id,company,position,url from job_raw where position LIKE %s and %s-savetime < 7*86400",('%'+title+'%',tod))
    jobinfo = cursor.fetchall()
    cursor.close()
    job_list = list()
    for each in jobinfo:
        job_list.append({'job_id':each[0] ,'company':each[1],'position':each[2],'url':each[3]})
    return job_list

# rec
def rec(selected_job):
    cursor = connection.cursor()
    cursor.execute("select job2_id from recommendation where job1_id = %s order by similarity desc limit 2,5",selected_job) #job1_id
    # cursor.execute("select job2_id from recommendation where job1_id = %s order by similarity desc limit 2,5",'2546120842')
    rec_id = cursor.fetchall()
    cursor.close()
    # print(rec_id)
    rec_id_list = list()
    for id in rec_id:
        rec_id_list.append(id[0])
    # print(rec_id_list)

    rec_job_list = list()
    for i in rec_id_list:
        # print(i)
        cursor = connection.cursor()
        cursor.execute("select company,position,url from job_raw where job_id = %s",i)
        j = cursor.fetchall()
        cursor.close()
        rec_job_list.append({'company':j[0][0],'position':j[0][1],'url':j[0][2]})
        # rec_job_list.append(list(cursor.fetchall()[0]))
    # print(rec_job_list)
    return rec_job_list
# print(rec('2546120842')) 

def job_score(job_id):
    # test = '2554018338' #2550746682,2546120842,2554018338
    cursor = connection.cursor()
    cursor.execute("select keyword_name,count from job_keywords join keywords on job_keywords.keyword_id = keywords.keyword_id where job_id = %s",job_id)
    counts = cursor.fetchall()
    cursor.close()
    # print(counts)
    skills = list()
    scores = list()
    for i in counts:
        if i[1] != 0:
            skills.append(i[0])
            scores.append(int(i[1]))
    # sort dict
    d = {'skills':skills,'scores':scores}
    newd = dict()
    for i in range(len(skills)):
        newd[skills[i]] = scores[i]
    sorted_d = dict(sorted(newd.items(), key=lambda item: item[1], reverse=True))
    # print(sorted_d)
    sorted_d = OrderedDict(sorted_d)
    keys = list(sorted_d)[0:5]
    # print(keys)
    items = list()
    for item in keys:
        items.append(sorted_d[item])
    # print(items)
    # print({'skills':keys,'scores':items})
    return {'skills':keys,'scores':items}
# print(job_score('2546120842'))
# print(job_score('2550746682'))
# print(job_score('2507709258'))
# {'skills': ['SQL', 'Python', 'Scala', 'ETL'], 'scores': [1.0, 1.0, 1.0, 1.0]}
# {'skills': ['SQL', 'Spark', 'data pipeline', 'Python', 'AWS'], 'scores': [1.25, 1.25, 1.25, 0.625, 0.625]}
def job_score_old(job_id):
    # cursor.execute("select `job_id`,`SQL`,`Python` ,`Spark`,`AWS`,`Java`,`Hadoop`,`Hive`, `Scala` ,`Kafka` ,`NoSQL` ,`Redshift` ,`Azure` ,`Linux` ,`Tableau` ,`Git` ,`Cassandra` ,`Airflow` ,`Snowflake` ,`Docker` ,`MySQL` ,`PostgreSQL` ,`C++` ,`MongoDB` ,`GCP` ,`Jenkins` ,`data pipeline` ,`data warehouse` ,`data modeling` ,`ETL` ,`API` ,`Perl` ,`Tensorflow` ,`Javascript` ,`Keras` from skill_score where job_id = %s",'2539683107') #2539683107,2546120842
    cursor = connection.cursor()
    cursor.execute("select `job_id`,`SQL`,`Python` ,`Spark`,`AWS`,`Java`,`Hadoop`,`Hive`, `Scala` ,`Kafka` ,`NoSQL` ,`Redshift` ,`Azure` ,`Linux` ,`Tableau` ,`Git` ,`Cassandra` ,`Airflow` ,`Snowflake` ,`Docker` ,`MySQL` ,`PostgreSQL` ,`C++` ,`MongoDB` ,`GCP` ,`Jenkins` ,`data pipeline` ,`data warehouse` ,`data modeling` ,`ETL` ,`API` ,`Perl` ,`Tensorflow` ,`Javascript` ,`Keras` ,`Html`,`Css` from skill_score where job_id = %s",job_id)
    score = cursor.fetchall()
    cursor.close()
    # print(score) #(('2546120842', 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),)
    score_list = list()
    items = list()
    try: 
        score_list.append({'job_id':score[0][0],'score':list(score[0][1:])})
        # print(score_list)
        d = dict()
        for i in range(len(score_list[0]['score'])):
            if score_list[0]['score'][i] != 0:
                d[skillset[i]] = score_list[0]['score'][i]
        # print(d)
        sorted_d = dict(sorted(d.items(), key=operator.itemgetter(1),reverse=True))
        sorted_d = OrderedDict(sorted_d)
    except:
        sorted_d = {}
    keys = list(sorted_d)[0:5]
    # print(keys)
    for item in keys:
        items.append(sorted_d[item])
    # print(items)
    if len(items) != 0:
        mean = sum(items)/len(items)
    # print(mean)
    else:
        mean = 1
    new_items = list()
    for i in items:
        new_items.append(i/mean) # normalize
    # print(new_items)
    # print(type(sorted_d)) #<class 'collections.OrderedDict'>
    # print({'skills':keys,'scores':new_items})
    return {'skills':keys,'scores':new_items}

def trend():
    today = str(date.today())
    last_year = str(datetime.now() - relativedelta(years=1))[:10]
    start_date = last_year
    end_data = today
    # 5/29
    url = 'https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=-480&req=%7B%22time%22:%222020-05-29+2021-05-29%22,%22resolution%22:%22WEEK%22,%22locale%22:%22zh-TW%22,%22comparisonItem%22:%5B%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+engineer%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+scientist%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+analyst%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22software+engineer%22%7D%5D%7D%7D%5D,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D%7D&token=APP6_UEAAAAAYLM98k6S8y20_KRmlJ8IpYRjn5PGZVeT&tz=-480'
    # 5/28
    # url = 'https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=-480&req=%7B%22time%22:%222020-05-28+2021-05-28%22,%22resolution%22:%22WEEK%22,%22locale%22:%22zh-TW%22,%22comparisonItem%22:%5B%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+engineer%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+scientist%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+analyst%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22software+engineer%22%7D%5D%7D%7D%5D,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D%7D&token=APP6_UEAAAAAYLGowr6zKvwGl3Lm9NEpeOgsAeWTGggX&tz=-480'
    # 5/27
    # url = 'https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=-480&req=%7B%22time%22:%222020-05-27+2021-05-27%22,%22resolution%22:%22WEEK%22,%22locale%22:%22zh-TW%22,%22comparisonItem%22:%5B%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+engineer%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+scientist%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+analyst%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22software+engineer%22%7D%5D%7D%7D%5D,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D%7D&token=APP6_UEAAAAAYLBtT0WEXyLvc0VrQnsoQPv9xnMyLkLv&tz=-480'
    # with day as parameter
    # url = 'https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=-480&req=%7B%22time%22:%22'+last_year+'+'+today+'%22,%22resolution%22:%22WEEK%22,%22locale%22:%22zh-TW%22,%22comparisonItem%22:%5B%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+engineer%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+scientist%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22data+analyst%22%7D%5D%7D%7D,%7B%22geo%22:%7B%22country%22:%22US%22%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22software+engineer%22%7D%5D%7D%7D%5D,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D%7D&token=APP6_UEAAAAAYLBtT0WEXyLvc0VrQnsoQPv9xnMyLkLv&tz=-480'
    request = requests.get(url)
    content = request.text

    # read file
    # with open ("json_us.txt", "r",encoding="utf-8") as f:
    #     content = f.read()

    # true = 'true'
    # contents = json.loads(content[6:])
    # contents = contents['default']['timelineData']
    # # print(len(contents)) # 52
    # trends = list()
    # de = list()
    # ds = list()
    # da = list()
    # se = list()
    # t = list()
    # for week in range(len(contents)):
    #     value_list = contents[week]['formattedValue']
    #     value_list = list(map(int, value_list))
    #     # print(value_list)
    #     time = contents[week]['formattedAxisTime']
    #     time = json.dumps(time)
    #     # trends.append(json.dumps({"value":value_list,"time":time}))
    #     # trends.append(json.dumps({"dataengineer":value_list[0],"datascientist":value_list[1],"dataanalyst":value_list[2],"softwareengineer":value_list[3],"time":time}))
        
    #     de.append(value_list[0])
    #     ds.append(value_list[1])
    #     da.append(value_list[2])
    #     se.append(value_list[3])
    #     time = contents[week]['formattedAxisTime']
    #     t.append(json.dumps(time))
    # trends.append(json.dumps({'de':de,'ds':ds,'da':da,'se':se,'time':t}))
    # return trends



    



