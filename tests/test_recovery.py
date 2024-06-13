# test_recovery.py
import os
from dotenv import load_dotenv
from restore.mysql_restore import mysql_restore
from restore.pgsql_restore import pgsql_restore

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
BACKUP_DIR = os.getenv('BACKUP_DIR')
LOG_DIR = os.getenv('LOG_DIR')

def test_mysql_restore():
    try:
        mysql_restore(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, BACKUP_DIR, LOG_DIR, 'full', MYSQL_DATABASE)
        print("MySQL restore successful")
    except Exception as e:
        print(f"Failed to restore MySQL: {e}")

def test_pgsql_restore():
    try:
        pgsql_restore(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, BACKUP_DIR, LOG_DIR, 'full', POSTGRES_DATABASE)
        print("PostgreSQL restore successful")
    except Exception as e:
        print(f"Failed to restore PostgreSQL: {e}")

if __name__ == "__main__":
    test_mysql_restore()
    test_pgsql_restore()
