import os
import unittest
import mysql.connector
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class TestConnection(unittest.TestCase):
    def test_mysql_connection(self):
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        self.assertIsNotNone(conn)
        conn.close()

    def test_pgsql_connection(self):
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            dbname=os.getenv('POSTGRES_DATABASE')
        )
        self.assertIsNotNone(conn)
        conn.close()

if __name__ == '__main__':
    unittest.main()
