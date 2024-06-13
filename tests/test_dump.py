# test_dump.py
import os
from dotenv import load_dotenv
from backup.mysql_backup import mysql_backup
from backup.pgsql_backup import pgsql_backup

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

def test_mysql_backup():
    try:
        mysql_backup(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, BACKUP_DIR, LOG_DIR, 'full', MYSQL_DATABASE)
        print("MySQL backup successful")
    except Exception as e:
        print(f"Failed to backup MySQL: {e}")

def test_pgsql_backup():
    try:
        pgsql_backup(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, BACKUP_DIR, LOG_DIR, 'full', POSTGRES_DATABASE)
        print("PostgreSQL backup successful")
    except Exception as e:
        print(f"Failed to backup PostgreSQL: {e}")

if __name__ == "__main__":
    test_mysql_backup()
    test_pgsql_backup()
