from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json

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

engine = create_engine(
    'mysql+pymysql://'+User+':'+Password+'@localhost/JHT',
    echo = True)
connection = engine.raw_connection()
cursor = connection.cursor()


# jobinfo
def jobinfo(title):
    cursor.execute("select company,position,status,posttime from Job where position LIKE %s and status LIKE 'Actively Hiring'",title)
    jobinfo = cursor.fetchall()
    joblist = list()
    for each in jobinfo:
        joblist.append({'company':each[0],'position':each[1],'hiring/salary range':each[2],'hiring/post':each[3]})
    return joblist
# print(jobinfo('data engineer')) #'data engineer'

# test
cursor.execute("select company,position from Job where position LIKE 'data engineer' limit 5")
info = cursor.fetchall()
# print('info: ',info)
"""
(
    ('Facebook621 reviews', 'Data Engineer'), 
    ('Bangura Solutions', 'DATA ENGINEER'), 
    ('Luxoft225 reviews', 'Data engineer'), 
    ('LPL Financial515 reviews', 'Data Engineer'), 
    ('Amazon.com Services LLC70,092 reviews', 'Data Engineer'), 
)

"""
# cursor.execute("select details from Job where position LIKE 'data engineer' limit 5")
cursor.execute("select `index`from Job limit 3")
print(cursor.fetchall())
# ((1,), (2,), (3,))
print('---------------')
cursor.execute("select details from Job limit 3")
details = cursor.fetchall()
print('how many data engineer: ', len(details))
jds = list()
for jd in details:
    jds.append(jd[0])

# TFIDF => recommend based on TFIDF (no keywords extracted)
start = time.perf_counter() 
vect = TfidfVectorizer(min_df=1, stop_words="english")                                                                                                                                                                                                   
tfidf = vect.fit_transform(jds)                                                                                                                                                                                                                   
pairwise_similarity = tfidf * tfidf.T 
# print('-----------------')
# print('pairwise_similarity: ',pairwise_similarity)
# print('-----------------')
pairwise_similarity = pairwise_similarity.toarray()
item_sim_list = list()
for item_sim_matrix in pairwise_similarity:
    # print(item_sim_matrix) #每個item和其他所有人的相似度矩陣 #[0.         0.         1.         0.39427569 0.        ]
    nonZeroIndexArray = np.nonzero(item_sim_matrix)
    data = list()
    for nonZeroIndex in nonZeroIndexArray[0]:
        sim_list = [{"id":str(nonZeroIndex),"similarity":item_sim_matrix[nonZeroIndex]}]
        data.extend(sim_list)  
    item_sim_list.append(json.dumps({'data': data}))
# print('item_sim_list: ',item_sim_list[0])
id_list = [i for i in range(len(item_sim_list))]
finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} second(s)')   

# keyword



"""
with connection:
    cursor = connection.cursor()
    back = cursor.executemany("INSERT INTO recommendation (selected_id,recommend_id) VALUES(%s,%s)", zip(id_list,item_sim_list)) 
    connection.commit()
    print(back)


pure word count => bad
from collections import Counter 
def count_words_fast(text):     
    text = text.lower() 
    skips = [".", ", ", ":", ";", "'", '"','\n','+','(',')'] 
    for ch in skips: 
        text = text.replace(ch, "") 
    word_counts = Counter(text.split(" ")) 
    return word_counts 
print(count_words_fast(details))
"""