import os
import unittest
from backup.mysql_backup import mysql_backup
from backup.pgsql_backup import pgsql_backup
from dotenv import load_dotenv

load_dotenv()

class TestDump(unittest.TestCase):
    def test_mysql_dump(self):
        mysql_backup(
            os.getenv('MYSQL_HOST'),
            os.getenv('MYSQL_USER'),
            os.getenv('MYSQL_PASSWORD'),
            os.getenv('BACKUP_DIR'),
            os.getenv('LOG_DIR'),
            'full',
            os.getenv('MYSQL_DATABASE')
        )

    def test_pgsql_dump(self):
        pgsql_backup(
            os.getenv('POSTGRES_HOST'),
            os.getenv('POSTGRES_USER'),
            os.getenv('POSTGRES_PASSWORD'),
            os.getenv('BACKUP_DIR'),
            os.getenv('LOG_DIR'),
            'full',
            os.getenv('POSTGRES_DATABASE')
        )

if __name__ == '__main__':
    unittest.main()
