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

sql = """CREATE TABLE `Jobs` (
`index` int AUTO_INCREMENT,
`position` varchar(255),
`company` varchar(255),
`location` varchar(255),
`status` varchar(255),
`posttime` varchar(255),
`savetodbtime` timestamp,
`details` longtext,
`url` varchar(255),
PRIMARY KEY (`index`)
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8
"""
cursor.execute(sql)
