import os
import pymysql
from dotenv import load_dotenv
load_dotenv()

Host = os.getenv("Host")
User = os.getenv("User")
Password = os.getenv("Password")
Path = os.getenv("Path")

connection = pymysql.connect(host=Host,
                             user=User,
                             password=Password,
                             database = 'JHT',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
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

sql = """CREATE TABLE `skill_match_radar` (
`id` int AUTO_INCREMENT,
`job_id` varchar(255),
`SQL` int,
`Python` int ,
`Java` int,
`Spark` int,
`AWS` int,
`ETL` int,
PRIMARY KEY (`id`),
FOREIGN KEY (`job_id`) REFERENCES job_raw(`job_id`) 
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

# sql = """CREATE TABLE `recommendation` (
# `id` int AUTO_INCREMENT,
# `job1_id` varchar(255),
# `job2_id` varchar(255),
# `similarity` float,
# PRIMARY KEY (`id`),
# FOREIGN KEY (`job1_id`) REFERENCES job_raw(`job_id`)
# ) 
# ENGINE=InnoDB DEFAULT CHARSET=utf8
# # """

cursor.execute(sql)

