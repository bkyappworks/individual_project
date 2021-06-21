import sqlalchemy
from sqlalchemy import create_engine
import os
import pymysql
from dotenv import load_dotenv
load_dotenv()

Host = os.getenv("Host")
User = os.getenv("User")
Password = os.getenv("Password")
Path = os.getenv("Path")
connection_string = 'mysql+pymysql://'+User+':'+Password+'@'+Host+':3306/JHT'
engine = create_engine(connection_string,pool_recycle=3600)
connection = engine.raw_connection()
cursor = connection.cursor()
# print(Host)
# print(User)

# connect to mysql
# connection = pymysql.connect(host=Host,
#                              user=User,
#                              password=Password,
#                              database = 'JHT',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# cursor = connection.cursor()


# sql = """CREATE DATABASE `JHT`
# """

# sql = """CREATE TABLE `rawjob` (
# `index` int AUTO_INCREMENT,
# `position` varchar(255),
# `company` varchar(255),
# `location` varchar(255),
# `details` longtext,
# PRIMARY KEY (`index`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """
# sql = """CREATE TABLE `Job` (
# `index` int AUTO_INCREMENT,
# `position` varchar(255),
# `company` varchar(255),
# `location` varchar(255),
# `status` varchar(255),
# `posttime` varchar(255),
# `savetodbtime` timestamp,
# `details` longtext,
# PRIMARY KEY (`index`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `TFIDF` (
# `id` int AUTO_INCREMENT,
# `job_1` varchar(255),
# `job_2` varchar(255),
# `similarity` varchar(255),
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `keyword` (
# `id` int AUTO_INCREMENT,
# `job1_id` varchar(255),
# `job2_id` varchar(255),
# `similarity` float,
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `Jobs` (
# `id` int AUTO_INCREMENT,
# `position` varchar(255),
# `company` varchar(255),
# `location` varchar(255),
# `hiringstatus` varchar(255),
# `posttime` varchar(255),
# `url` varchar(255),
# `description` longtext,
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `skill_sim` (
# `id` int AUTO_INCREMENT,
# `job1_id` varchar(255),
# `job2_id` varchar(255),
# `similarity` float,
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `etl_test` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `position` varchar(255),
# `company` varchar(255),
# `experience` json,
# `salary` json,
# `SQL` int,
# `Python` int,
# `Spark` int,
# `AWS` int,
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """
# sql = """CREATE TABLE `etl_test1` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `position` varchar(255),
# `company` varchar(255),
# `experience` json,
# `salary` json,
# `SQL` int,
# `Python` int ,
# `Spark` int,
# `AWS` int,
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `skill_match` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `position` varchar(255),
# `company` varchar(255),
# `SQL` int,
# `Python` int ,
# `Java` int,
# `Spark` int,
# `AWS` int,
# `ETL` int,
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """
#`jobid`,`position`,`company`,`SQL`,`Python`,`Java`,`Spark`,`AWS`,`ETL`

# sql = """CREATE TABLE `brief` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `position` varchar(255),
# `company` varchar(255),
# `brief` json,
# `year` json,
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """
#`job_id`,`position`,`company`,`brief`,`year`

# sql = """CREATE TABLE `Joball` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `position` varchar(255),
# `company` varchar(255),
# `location` varchar(255),
# `hiringstatus` varchar(255),
# `posttime` varchar(255),
# `savetime` varchar(255),
# `url` varchar(255),
# `description` longtext,
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `recommendation` (
# `id` int AUTO_INCREMENT,
# `job1_id` varchar(255),
# `job2_id` varchar(255),
# `similarity` float,
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `skill_score` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `position` varchar(255),
# `company` varchar(255),
# `SQL` int,
# `Python` int ,
# `Java` int,
# `Spark` int,
# `AWS` int,
# `ETL` int,
# PRIMARY KEY (`id`),
# FOREIGN KEY (`job_id`) REFERENCES Joball(`job_id`) 
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `jd_brief` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `position` varchar(255),
# `company` varchar(255),
# `brief` json,
# `year` json,
# PRIMARY KEY (`id`),
# FOREIGN KEY (`job_id`) REFERENCES Joball(`job_id`) 
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `recommendations` (
# `id` int AUTO_INCREMENT,
# `job1_id` varchar(255),
# `job2_id` varchar(255),
# `similarity` float,
# PRIMARY KEY (`id`),
# FOREIGN KEY (`job1_id`) REFERENCES Joball(`job_id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `work_years_required` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `years_of_experience` longtext,
# PRIMARY KEY (`id`),
# FOREIGN KEY (`job_id`) REFERENCES job_raw(`job_id`) 
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `exp_required` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `experience_required` longtext,
# PRIMARY KEY (`id`),
# FOREIGN KEY (`job_id`) REFERENCES job_raw(`job_id`) 
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `skill_match_radar` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `SQL` int,
# `Python` int ,
# `Java` int,
# `Spark` int,
# `AWS` int,
# `ETL` int,
# PRIMARY KEY (`id`),
# FOREIGN KEY (`job_id`) REFERENCES job_raw(`job_id`) 
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `recommendation` (
# `id` int AUTO_INCREMENT,
# `job1_id` varchar(255),
# `job2_id` varchar(255),
# `similarity` float,
# PRIMARY KEY (`id`),
# FOREIGN KEY (`job1_id`) REFERENCES job_raw(`job_id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """


# 'SQL','Python','Spark','AWS','Java','Hadoop','Hive', 'Scala','Kafka','NoSQL','Redshift','Azure',
# 'Linux','R','Tableau','Oracle','Git','Cassandra','Airflow','Snowflake','Docker','MySQL','PostgreSQL',
# 'C++','MongoDB','GCP','Jenkins','data pipeline','data warehouse','data modeling','ETL','API','Perl','Go','Tensorflow','Javascript','Keras'

# sql = """CREATE TABLE `skill_score` (
# `id` int AUTO_INCREMENT,
# `job_id` varchar(255),
# `SQL` int,
# `Python` int ,
# `Spark` int,
# `AWS` int,
# `Java` int,
# `Hadoop` int,
# `Hive` int, 
# `Scala` int,
# `Kafka` int,
# `NoSQL` int,
# `Redshift` int,
# `Azure` int,
# `Linux` int,
# `Tableau` int,
# `Git` int,
# `Cassandra` int,
# `Airflow` int,
# `Snowflake` int,
# `Docker` int,
# `MySQL` int,
# `PostgreSQL` int,
# `C++` int,
# `MongoDB` int,
# `GCP` int,
# `Jenkins` int,
# `data pipeline` int,
# `data warehouse` int,
# `data modeling` int,
# `ETL` int,
# `API` int,
# `Perl` int,
# `Tensorflow` int,
# `Javascript` int,
# `Keras` int,
# `Html` int,
# `Css` int,
# PRIMARY KEY (`id`),
# FOREIGN KEY (`job_id`) REFERENCES job_raw(`job_id`) 
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

# sql = """CREATE TABLE `keywords` (
# `id` int AUTO_INCREMENT,
# `keyword_id` varchar(255) UNIQUE,
# `keyword_name` varchar(255),
# PRIMARY KEY (`id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# """

sql = """CREATE TABLE `job_keywords` (
`id` int AUTO_INCREMENT,
`job_id` varchar(255),
`keyword_id` varchar(255),
`count` int,
PRIMARY KEY (`id`)
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

cursor.execute(sql)

# sql =  """
# INSERT INTO `keywords` (keyword_id,keyword_name) 
# VALUES(%s,%s)
# """

# data = [
#         [1,'SQL'],[2,'Python'],[3,'Spark'],[4,'AWS'],[5,'Java'],[6,'Hadoop'],[7,'Hive'],[8,'Kafka'],[9,'NoSQL'],[10,'Redshift'],
#         [11,'Azure'],[12,'Linux'],[13,'Tableau'],[14,'Cassandra'],[15,'Airflow'],[16,'Snowflake'],[17,'Docker'],[18,'MySQL'],[19,'PostgreSQL'],
#         [20,'C++'],[21,'MongoDB'],[22,'GCP'],[23,'Jenkins'],[24,'data pipeline'],[25,'data warehouse'],[26,'data modeling'],[27,'ETL'],[28,'API'],[29,'Perl'],
#         [30,'Tensorflow'],[31,'Keras'],[32,'Javascript'],[33,'Html'],[34,'Css'],[35,'React-JS'],[36,'Swift'],[37,'Kotlin'],[38,'SDK'],[39,'Agile'],[40,'React']
#     ]
# back = cursor.executemany(sql,data)
# connection.commit()
# print(back) #40






