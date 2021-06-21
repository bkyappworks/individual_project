from collections import Counter
from numpy import dot
from numpy.linalg import norm
import json

import sqlalchemy
from sqlalchemy import create_engine
import re, time, pymysql.cursors, pymysql
import random
import os
from dotenv import load_dotenv
load_dotenv()

Host = os.getenv("Host")
User = os.getenv("User")
Password = os.getenv("Password")
Path = os.getenv("Path")

connection_string = 'mysql+pymysql://'+User+':'+Password+'@'+Host+':3306/JHT'
engine = create_engine(connection_string, echo = True, pool_recycle=3600)
connection = engine.raw_connection()
cursor = connection.cursor()

# test
test = 3
test_id = '2550755919'

import time
cal_after = int(round(time.time()-86400*1,0))
# print(cal_after) # 1623412584 6/12

skillset = list()
cursor.execute("select keyword_name from keywords") 
skills = cursor.fetchall()
for skill in skills:
    skillset.append(skill[0])
# skillset = [
#         'SQL','Python','Spark','AWS','Java','Hadoop','Hive','Kafka','NoSQL','Redshift',
#         'Azure','Linux','Tableau','Cassandra','Airflow','Snowflake','Docker','MySQL','PostgreSQL',
#         'C++','MongoDB','GCP','Jenkins','data pipeline','data warehouse','data modeling','ETL','API','Perl',
#         'Tensorflow','Keras','Javascript','Html','Css','React-JS','Swift','Kotlin','SDK','Agile','React'
#     ]

def count_keywords():
    # cursor.execute("select job_id,description from job_raw limit %s",test) 
    cursor.execute("select job_id,description from job_raw where savetime > %s",cal_after) 
    info = list(cursor.fetchall())

    ids = list() #['2488303735', '2492689892', '2497731654']
    kw = list()
    insert = list()
    skillsets = [i.lower() for i in skillset]
    for i in info:
        id = i[0]
        jd = i[1].lower()
        ids.append(id)
        count_skill_dict = dict((x,jd.count(x)) for x in set(skillsets))
        kw.append(count_skill_dict)

    for i in range(len(ids)):
        for j in range(len(skillsets)):
            insert.append([ids[i],j+1,kw[i][skillsets[j]]])
            # kw[i]['sql'],kw[i]['python'],kw[i]['spark'],kw[i]['aws'],kw[i]['java'],
            # kw[i]['hadoop'],kw[i]['hive'],kw[i]['kafka'],kw[i]['nosql'],kw[i]['redshift'],
            # kw[i]['azure'],kw[i]['linux'],kw[i]['tableau'],kw[i]['cassandra'],
            # kw[i]['airflow'],kw[i]['snowflake'],kw[i]['docker'],kw[i]['mysql'],
            # kw[i]['postgresql'],kw[i]['c++'],kw[i]['mongodb'],kw[i]['gcp'],kw[i]['jenkins'],
            # kw[i]['data pipeline'],kw[i]['data warehouse'],kw[i]['data modeling'],
            # kw[i]['etl'],kw[i]['api'],kw[i]['perl'],kw[i]['tensorflow'],kw[i]['keras'],
            # kw[i]['javascript'],kw[i]['html'],kw[i]['css'],kw[i]['react-js'],kw[i]['swift'],
            # kw[i]['kotlin'],kw[i]['sdk'],kw[i]['agile'],kw[i]['react'])
    # print(insert[0])
    return insert

def save_keywords(data):
    sql = "INSERT INTO job_keywords (`job_id`,`keyword_id`,`count`) VALUES(%s,%s,%s)"
    back = cursor.executemany(sql, data)  
    connection.commit()
    print('Items save to db: ',back)
# save
# save_keywords(count_keywords())

# skill_score table
def skill_score():
    all = list()
    kw = list()
    infos = list()
    # cursor.execute("select job_id,description from job_raw limit %s",test) 
    cursor.execute("select job_id,description from job_raw where savetime > %s",cal_after) 
    # cursor.execute("select job_id,description from job_raw") 
    info = list(cursor.fetchall())
    # print(info)
    for i in info:
        i = i[0]
        infos.append(i)
    # print(infos)
    # kw
    # cursor.execute("select description from job_raw limit %s",test) 
    cursor.execute("select description from job_raw where savetime > %s",cal_after) 
    # cursor.execute("select description from job_raw")
    jds = cursor.fetchall()
    # print(jds[0])

    for jd in jds: 
        jd = jd[0].lower()
        skillset = [
            'SQL','Python','Spark','AWS','Java','Hadoop','Hive','Scala','Kafka','NoSQL','Redshift',
            'Azure','Linux','Tableau','Git','Cassandra','Airflow','Snowflake','Docker','MySQL','PostgreSQL',
            'C++','MongoDB','GCP','Jenkins','data pipeline','data warehouse','data modeling','ETL','API','Perl',
            'Tensorflow','Javascript','Keras','Html','Css'
        ]  
        skillsets = [i.lower() for i in skillset]
        count_skill_dict = dict((x,jd.count(x)) for x in set(skillsets))
        kw.append(count_skill_dict)
    # print(kw)
    for i in range(len(infos)):
        # print(infos[i])
        all.append([
            infos[i],kw[i]['sql'],kw[i]['python'],kw[i]['spark'],kw[i]['aws'],kw[i]['java'],kw[i]['hadoop'],
            kw[i]['hive'],kw[i]['scala'],kw[i]['kafka'],kw[i]['nosql'],kw[i]['redshift'],
            kw[i]['azure'],kw[i]['linux'],kw[i]['tableau'],kw[i]['git'],kw[i]['cassandra'],
            kw[i]['airflow'],kw[i]['snowflake'],kw[i]['docker'],kw[i]['mysql'],kw[i]['postgresql'],
            kw[i]['c++'],kw[i]['mongodb'],kw[i]['gcp'],kw[i]['jenkins'],kw[i]['data pipeline'],kw[i]['data warehouse'],
            kw[i]['data modeling'],kw[i]['etl'],kw[i]['api'],kw[i]['perl'],kw[i]['tensorflow'],kw[i]['javascript'],kw[i]['keras'],kw[i]['html'],kw[i]['css']])
    # print(all[0:3])
    # print(len(all))
    return all

def save_score(data): 
    sql = "INSERT INTO skill_score (`job_id`,`SQL`,`Python` ,`Spark`,`AWS`,`Java`,`Hadoop`,`Hive`, `Scala` ,`Kafka` ,`NoSQL` ,`Redshift` ,`Azure` ,`Linux` ,`Tableau` ,`Git` ,`Cassandra` ,`Airflow` ,`Snowflake` ,`Docker` ,`MySQL` ,`PostgreSQL` ,`C++` ,`MongoDB` ,`GCP` ,`Jenkins` ,`data pipeline` ,`data warehouse` ,`data modeling` ,`ETL` ,`API` ,`Perl` ,`Tensorflow` ,`Javascript` ,`Keras`,`Html`,`Css` ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    back = cursor.executemany(sql, data)  
    connection.commit()
    print('Items save to db: ',back)
# save successfully
# save_score(skill_score())

def work_years_required():
    all = list()
    cursor.execute("select job_id,description from job_raw where savetime > %s",cal_after) 
    # cursor.execute("select job_id,description from job_raw limit %s",test) 
    infos = list(cursor.fetchall())
    for i in range(len(infos)):
        job_id = infos[i][0]
        jd = infos[i][1]
        # print(job_id)
        year_of_exp = re.findall(
            r'[0-9].*years.*experience.*',
            jd,
            re.IGNORECASE)
        if len(year_of_exp) >= 1:
            for i in range(len(year_of_exp)):
                all.append([job_id,year_of_exp[i]])
        else:
            all.append([job_id,'Not Specified'])
    # print(all)
    return all

def save_year(data):
    sql = "INSERT INTO work_years_required (`job_id`,`years_of_experience`) VALUES(%s,%s)"
    back = cursor.executemany(sql, data)  
    connection.commit()
    print('Items save to db: ',back)
# save successfully
# save_year(work_years_required())

def exp_required():
    all = list()
    cursor.execute("select job_id,description from job_raw where savetime > %s",cal_after) 
    # cursor.execute("select job_id,description from job_raw limit %s",test) 
    infos = list(cursor.fetchall())
    for i in range(len(infos)):
        job_id = infos[i][0]
        jd = infos[i][1]
        # print(job_id)
        exp = re.findall(
                r'years.*|experience in.*|experience with.*|experience of.*|skill with.*|skill including.*|understand.*|programming.*\.?$',
                jd,
                re.IGNORECASE)
        if len(exp) >= 1:
            for i in range(len(exp)):
                all.append([job_id,exp[i]])
        else:
            all.append([job_id,'Not Specified'])
    # print(all)
    return all

def save_exp(data):
    sql = "INSERT INTO exp_required (`job_id`,`experience_required`) VALUES(%s,%s)"
    back = cursor.executemany(sql, data)  
    connection.commit()
    print('Items save to db: ',back)
# save successfully
# save_exp(exp_required())

def cal_sim():
    skillset = list()
    cursor.execute("select keyword_name from keywords") 
    skills = cursor.fetchall()
    for skill in skills:
        skillset.append(skill[0])
    skillsets = [i.lower() for i in skillset]
    cursor.execute("select job_id,description from job_raw where savetime > %s",cal_after) 
    raw = cursor.fetchall()
    jobs = list()
    kw = list()
    insert_all = list()
    job_ids = list()
    for job in raw:
        job_ids.append(job[0])
        jobs.append(job[1])
    # print(jobs)
    for jd in jobs:
        jd = jd.lower()
        count_skill_dict = dict((x,jd.count(x)) for x in set(skillsets))
        kw.append(count_skill_dict)
    for i in range(len(jobs)):
        insert_all.append(
            [kw[i]['sql'],kw[i]['python'],kw[i]['spark'],kw[i]['aws'],kw[i]['java'],
            kw[i]['hadoop'],kw[i]['hive'],kw[i]['kafka'],kw[i]['nosql'],kw[i]['redshift'],
            kw[i]['azure'],kw[i]['linux'],kw[i]['tableau'],kw[i]['cassandra'],
            kw[i]['airflow'],kw[i]['snowflake'],kw[i]['docker'],kw[i]['mysql'],
            kw[i]['postgresql'],kw[i]['c++'],kw[i]['mongodb'],kw[i]['gcp'],kw[i]['jenkins'],
            kw[i]['data pipeline'],kw[i]['data warehouse'],kw[i]['data modeling'],
            kw[i]['etl'],kw[i]['api'],kw[i]['perl'],kw[i]['tensorflow'],kw[i]['keras'],
            kw[i]['javascript'],kw[i]['html'],kw[i]['css'],kw[i]['react-js'],kw[i]['swift'],
            kw[i]['kotlin'],kw[i]['sdk'],kw[i]['agile'],kw[i]['react']]
        )
    sim = list()
    for i in range(len(insert_all)-1):
        # print(insert_all[i][1:])
        for j in range(len(insert_all)):
            if norm(insert_all[i][1:]) != 0 and norm(insert_all[j][1:]) != 0:
                try: 
                    similarity = dot(insert_all[i][1:], insert_all[j][1:])/(norm(insert_all[i][1:]) * norm(insert_all[j][1:]))
                    similarity = round(similarity,3)
                    sim.append([job_ids[i],job_ids[j],similarity])
                except:
                    similarity = -1
                    sim.append([job_ids[i],job_ids[j],similarity])
    return sim
    # print(sim)

def save_sim(data):
    back = cursor.executemany("INSERT INTO recommendation (job1_id,job2_id,similarity) VALUES(%s,%s,%s)", data) 
    connection.commit()
    print('Items save to db: ',back)
# save successfully
# save_sim(cal_sim())

