# test_backup_and_restore.py
import unittest
from tests import test_connection
from test_dump import test_mysql_backup, test_pgsql_backup
from test_recovery import test_mysql_restore, test_pgsql_restore

class TestDatabaseBackupAndRestore(unittest.TestCase):
    def test_mysql_connection(self):
        test_connection()

    def test_pgsql_connection(self):
        test_connection()

    def test_mysql_backup(self):
        test_mysql_backup()

    def test_pgsql_backup(self):
        test_pgsql_backup()

    def test_mysql_restore(self):
        test_mysql_restore()

    def test_pgsql_restore(self):
        test_pgsql_restore()

if __name__ == '__main__':
    unittest.main()
