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
engine = create_engine(connection_string,echo = True)
connection = engine.raw_connection()
cursor = connection.cursor()

# jobinfo
def jobinfo(title):
    cursor.execute("select job_id,company,position,url from job_raw where position LIKE %s order by savetime desc",'%'+title+'%')
    jobinfo = cursor.fetchall()
    job_list = list()
    for each in jobinfo:
        job_list.append({'job_id':each[0] ,'company':each[1],'position':each[2],'url':each[3]})
    return job_list

# rec
def rec(selected_job):
    cursor.execute("select job2_id from recommendation where job1_id = %s order by similarity desc limit 2,5",selected_job) #job1_id
    # cursor.execute("select job2_id from recommendation where job1_id = %s order by similarity desc limit 2,5",'2546120842')
    rec_id = cursor.fetchall()
    # print(rec_id)
    rec_id_list = list()
    for id in rec_id:
        rec_id_list.append(id[0])
    # print(rec_id_list)

    rec_job_list = list()
    for i in rec_id_list:
        # print(i)
        cursor.execute("select company,position,url from job_raw where job_id = %s",i)
        j = cursor.fetchall()
        rec_job_list.append({'company':j[0][0],'position':j[0][1],'url':j[0][2]})
        # rec_job_list.append(list(cursor.fetchall()[0]))
    # print(rec_job_list)
    return rec_job_list
# print(rec('2546120842'))

def job_score_old(job_id):
    cursor.execute("select `SQL`,`Python`,`Java`,`Spark`,`AWS`,`ETL` from skill_match_radar where job_id = %s",job_id)
    # cursor.execute("select `SQL`,`Python`,`Java`,`Spark`,`AWS`,`ETL` from skill_score where job_id = %s",'2546120842')
    score = cursor.fetchall()
    # print(score)
    score_list = list()
    # score_list.append({'SQL':score[0][0],'Python':score[0][1],'Java':score[0][2],'Spark':score[0][3],'AWS':score[0][4],'ETL':score[0][5]})
    score_list.append({'data':score})
    print(score_list)
    return score_list
# job_score_old('2548631341')

def job_score(job_id):
    skillset = [
        'SQL','Python','Spark','AWS','Java','Hadoop','Hive','Scala','Kafka','NoSQL','Redshift',
        'Azure','Linux','Tableau','Git','Cassandra','Airflow','Snowflake','Docker','MySQL','PostgreSQL',
        'C++','MongoDB','GCP','Jenkins','data pipeline','data warehouse','data modeling','ETL','API','Perl',
        'Tensorflow','Javascript','Keras','Html','Css'
    ]  
    # cursor.execute("select `job_id`,`SQL`,`Python` ,`Spark`,`AWS`,`Java`,`Hadoop`,`Hive`, `Scala` ,`Kafka` ,`NoSQL` ,`Redshift` ,`Azure` ,`Linux` ,`Tableau` ,`Git` ,`Cassandra` ,`Airflow` ,`Snowflake` ,`Docker` ,`MySQL` ,`PostgreSQL` ,`C++` ,`MongoDB` ,`GCP` ,`Jenkins` ,`data pipeline` ,`data warehouse` ,`data modeling` ,`ETL` ,`API` ,`Perl` ,`Tensorflow` ,`Javascript` ,`Keras` from skill_score where job_id = %s",'2539683107') #2539683107,2546120842
    cursor.execute("select `job_id`,`SQL`,`Python` ,`Spark`,`AWS`,`Java`,`Hadoop`,`Hive`, `Scala` ,`Kafka` ,`NoSQL` ,`Redshift` ,`Azure` ,`Linux` ,`Tableau` ,`Git` ,`Cassandra` ,`Airflow` ,`Snowflake` ,`Docker` ,`MySQL` ,`PostgreSQL` ,`C++` ,`MongoDB` ,`GCP` ,`Jenkins` ,`data pipeline` ,`data warehouse` ,`data modeling` ,`ETL` ,`API` ,`Perl` ,`Tensorflow` ,`Javascript` ,`Keras` ,`Html`,`Css` from skill_score where job_id = %s",job_id)
    score = cursor.fetchall()
    # print(score)
    score_list = list()
    items = list()
    try: 
        score_list.append({'job_id':score[0][0],'score':list(score[0][1:])})
        # print(score_list)
        d = dict()
        for i in range(len(score_list[0]['score'])):
            # print(i)
            # print(score_list[0]['score'][i])
            if score_list[0]['score'][i] != 0:
                print(skillset[i])
                # print(score[0][i])
                d[skillset[i]] = score_list[0]['score'][i]
                # d[skillset[i]] = score[i]
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
# job_score('2546120842')
# job_score('2550746682')
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
    with open ("json_us.txt", "r",encoding="utf-8") as f:
        content = f.read()

    true = 'true'
    contents = json.loads(content[6:])
    contents = contents['default']['timelineData']
    # print(len(contents)) # 52
    trends = list()
    de = list()
    ds = list()
    da = list()
    se = list()
    t = list()
    for week in range(len(contents)):
        value_list = contents[week]['formattedValue']
        value_list = list(map(int, value_list))
        # print(value_list)
        time = contents[week]['formattedAxisTime']
        time = json.dumps(time)
        # trends.append(json.dumps({"value":value_list,"time":time}))
        # trends.append(json.dumps({"dataengineer":value_list[0],"datascientist":value_list[1],"dataanalyst":value_list[2],"softwareengineer":value_list[3],"time":time}))
        
        de.append(value_list[0])
        ds.append(value_list[1])
        da.append(value_list[2])
        se.append(value_list[3])
        time = contents[week]['formattedAxisTime']
        t.append(json.dumps(time))
    trends.append(json.dumps({'de':de,'ds':ds,'da':da,'se':se,'time':t}))
    return trends



    



