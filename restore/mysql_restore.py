import os
import mysql.connector
import logging

class MySQLRestore:
    def __init__(self, host, user, password, backup_dir, log_dir, new_database=None):
        self.host = host
        self.user = user
        self.password = password
        self.backup_dir = backup_dir
        self.log_dir = log_dir
        self.new_database = new_database
        self.conn = mysql.connector.connect(host=host, user=user, password=password)
        self.cursor = self.conn.cursor()
        self.setup_logging()
        self.ensure_directories_exist()

        if new_database:
            self.create_database(new_database)
            self.conn.database = new_database

    def setup_logging(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.logger = logging.getLogger('mysql_restore')
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(os.path.join(self.log_dir, 'mysql_restore.log'))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def ensure_directories_exist(self):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_database(self, db_name):
        try:
            self.cursor.execute(f"CREATE DATABASE {db_name}")
            self.logger.info(f"Database {db_name} created successfully.")
        except mysql.connector.Error as err:
            self.logger.error(f"Failed creating database {db_name}: {err}")

    def restore_structure(self):
        self.logger.info("Starting MySQL structure restore")
        backup_file = self.get_latest_backup('structure')
        with open(backup_file, 'r') as f:
            sql_script = f.read()
            sql_commands = sql_script.split(';')
            for command in sql_commands:
                if command.strip():
                    try:
                        self.cursor.execute(command)
                    except mysql.connector.Error as err:
                        self.logger.error(f"Error executing SQL: {command.strip()} - {err}")
        self.logger.info(f"MySQL structure restored from {backup_file}")

    def restore_data(self):
        self.logger.info("Starting MySQL data restore")
        backup_file = self.get_latest_backup('data')
        with open(backup_file, 'r') as f:
            sql_script = f.read()
            sql_commands = sql_script.split(';')
            for command in sql_commands:
                if command.strip():
                    try:
                        self.cursor.execute(command)
                    except mysql.connector.Error as err:
                        self.logger.error(f"Error executing SQL: {command.strip()} - {err}")
        self.logger.info(f"MySQL data restored from {backup_file}")

    def restore_full(self):
        self.logger.info("Starting full MySQL restore")
        self.restore_structure()
        self.restore_data()

    def close(self):
        self.cursor.close()
        self.conn.close()
        self.logger.info("MySQL restore connection closed")

    def get_latest_backup(self, backup_type):
        files = os.listdir(self.backup_dir)
        backup_files = [f for f in files if backup_type in f]
        if not backup_files:
            raise FileNotFoundError(f"No {backup_type} backup files found in {self.backup_dir}")
        latest_backup = max(backup_files, key=lambda x: os.path.getctime(os.path.join(self.backup_dir, x)))
        return os.path.join(self.backup_dir, latest_backup)

def mysql_restore(host, user, password, backup_dir, log_dir, restore_type, new_database=None):
    restore = MySQLRestore(host, user, password, backup_dir, log_dir, new_database)
    if restore_type == 'structure':
        restore.restore_structure()
    elif restore_type == 'data':
        restore.restore_data()
    elif restore_type == 'full':
        restore.restore_full()
    restore.close()
