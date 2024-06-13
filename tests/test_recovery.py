import os
import unittest
from restore.mysql_restore import mysql_restore
from restore.pgsql_restore import pgsql_restore
from dotenv import load_dotenv

load_dotenv()

class TestRecovery(unittest.TestCase):
    def test_mysql_recovery(self):
        mysql_restore(
            os.getenv('MYSQL_HOST'),
            os.getenv('MYSQL_USER'),
            os.getenv('MYSQL_PASSWORD'),
            os.getenv('BACKUP_DIR'),
            os.getenv('LOG_DIR'),
            'full',
            os.getenv('MYSQL_DATABASE')
        )

    # def test_pgsql_recovery(self):
    #     pgsql_restore(
    #         os.getenv('POSTGRES_HOST'),
    #         os.getenv('POSTGRES_USER'),
    #         os.getenv('POSTGRES_PASSWORD'),
    #         os.getenv('BACKUP_DIR'),
    #         os.getenv('LOG_DIR'),
    #         'full',
    #         os.getenv('POSTGRES_DATABASE')
    #     )

if __name__ == '__main__':
    unittest.main()
