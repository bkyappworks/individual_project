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

engine = create_engine(
    'mysql+pymysql://'+User+':'+Password+'@localhost/JHT',
    echo = True)
connection = engine.raw_connection()
cursor = connection.cursor()

test = 20

# skill_score table
def skill_match():
    all = list()
    kw = list()
    infos = list()
    # cursor.execute("select job_id,position,company from job_raw limit %s",test) 
    cursor.execute("select job_id from job_raw") 
    info = list(cursor.fetchall())
    # print(info)
    for i in info:
        i = list(i)
        infos.append(i)
    # print(infos) # [[1, 'Data Engineer', 'American Express'], [2, 'Data Engineer', 'Apple'], [3, 'Data Engineer', 'HqO']]

    # kw
    # cursor.execute("select description from Jobs limit %s",test) 
    cursor.execute("select description from job_raw") 
    jds = cursor.fetchall()

    for jd in jds: 
        jd = jd[0]
        skillset = ['SQL','Python','Java','Spark','AWS','ETL']  
        count_skill = [jd.count(x) for x in set(skillset)]
        # print(count_skill) #
        dicts = dict((x,jd.count(x)) for x in set(skillset))
        # print(dicts)
        kw.append(count_skill)
    # print(kw) #[[1, 1, 4, 1, 0, 1], [1, 0, 2, 1, 0, 0], [0, 2, 1, 0, 0, 1]]

    for i in range(len(infos)):
        com = infos[i]+kw[i]
        all.append(com)

    print(len(all))
    print(all[:2])
    return all
# print(skill_score()) #[['2546120842', 'Data Engineer', 'Facebook', 1, 1, 0, 1, 0, 0], ['2539683107', 'Data Engineer', 'Slack', 3, 1, 0, 3, 0, 1], ['2528321227', 'Data Engineer', 'Tesla', 3, 5, 2, 1, 0, 4]]
def save_match(data): #INSERT INTO skill_match (`job_id`,`position`,`company`,`SQL`,`Python`,`Java`,`Spark`,`AWS`,`ETL`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
    sql = "INSERT INTO skill_match_radar (`job_id`,`SQL`,`Python`,`Java`,`Spark`,`AWS`,`ETL`) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    back = cursor.executemany(sql, data)  
    connection.commit()
    print('Items save to db: ',back)

# save successfully
# save_match(skill_match())

def work_years_required():
    all = list()
    cursor.execute("select job_id,description from job_raw") 
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
    cursor.execute("select job_id,description from job_raw") 
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


# too few
# cursor.execute("select description from job_raw limit %s",test) 
# cursor.execute("select description from job_raw") 
# jds = cursor.fetchall()
# for jd in jds:
#     salary = re.findall(r'\$.*bonus|\$.*pay|\$.*depend.*',jd[0])
#     if salary:
#         print('salary: ',salary)


def cal_sim():
    # cursor.execute("select description from Joball limit %s",test) 
    cursor.execute("select description from job_raw") 
    details = cursor.fetchall()

    skillset = [
        'SQL','Python','Spark','AWS','Java','Hadoop','Hive', 'Scala','Kafka','NoSQL','Redshift','Azure',
        'Linux','R','Tableau','Oracle','Git','Cassandra','Airflow','Snowflake','MySQL','PostgreSQL',
        'C++','MongoDB','GCP','data pipeline','data warehouse','ETL','migration','architectures',
        'distributed','API','Perl','C','Go','agile'
    ]    

    insert_all = []
    cnt = 0
    for detail in details:
        cnt+= 1
        # try:
        skills = re.findall(
            r'years.*|experience.*|skill.*|responsibilities.*|responsibility.*|background.*|understand.*|programming.*',
            detail[0],
            re.IGNORECASE|re.DOTALL)
        # print(cnt) 
        if len(skills) >=1:
            count_skill = [skills[0].count(x) for x in set(skillset)]
            # print('count_skill: ',count_skill)
            insert_all.append(count_skill)
        else:
            count_skill = [-1]
            # print('count_skill: ',count_skill)
            insert_all.append(count_skill) 
    # print('length: ',len(insert_all)) 
    # print(insert_all[0:3])
    id_list = []
    # cursor.execute("select job_id from Joball limit %s",test) 
    cursor.execute("select job_id from job_raw") 
    job_ids = cursor.fetchall()
    for id in job_ids:
        id_list.append(id[0])
    # print('job_ids: ',id_list)

    sim = list()
    for i in range(len(insert_all)-1):
        for j in range(len(insert_all)):
            if norm(insert_all[i]) != 0 and norm(insert_all[j]) != 0:
                # print(id_list[i],id_list[j])
                try: 
                    similarity = dot(insert_all[i], insert_all[j])/(norm(insert_all[i]) * norm(insert_all[j]))
                    sim.append([id_list[i],id_list[j],similarity])
                except:
                    similarity = -1
                    sim.append([id_list[i],id_list[j],similarity])
    print('sim: ',len(sim))
    return sim

def save_sim(data):
    # back = cursor.executemany("INSERT INTO skill_sim (job1_id,job2_id,similarity) VALUES(%s,%s,%s)", data) 
    back = cursor.executemany("INSERT INTO recommendation (job1_id,job2_id,similarity) VALUES(%s,%s,%s)", data) 
    connection.commit()
    print('Items save to db: ',back)
# save successfully
save_sim(cal_sim())


