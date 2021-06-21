import unittest
from models import job_score

import sqlalchemy
from sqlalchemy import create_engine
import re, time, pymysql.cursors, pymysql
import os
from dotenv import load_dotenv
load_dotenv()

Host = "localhost"
User = "root"
Password = "Myp@ss123"
# Host = os.getenv("Host")
# User = os.getenv("User")
# Password = os.getenv("Password")
# Path = os.getenv("Path")

connection_string = 'mysql+pymysql://'+User+':'+Password+'@'+Host+':3306/JHT'
engine = create_engine(connection_string,pool_recycle=3600)
connection = engine.raw_connection()
cursor = connection.cursor()


class TestFunctionMethods(unittest.TestCase):

    def test_job_score_general(self):
        actual = job_score('2546120842')
        expected = {'skills': ['SQL', 'Python', 'ETL'], 'scores': [1, 1, 1]}
        self.assertEqual(actual,expected)

    def test_job_score_general_2(self):
        actual = job_score('2550746682')
        expected = {'skills': ['SQL', 'Spark', 'data pipeline', 'Python', 'AWS'], 'scores': [2, 2, 2, 1, 1]}
        self.assertEqual(actual,expected)

    def test_job_score_without_scores(self):
        actual = job_score('2507709258')
        expected = {'skills': [], 'scores': []}
        self.assertEqual(actual,expected)


    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()