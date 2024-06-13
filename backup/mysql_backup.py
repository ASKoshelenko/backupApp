import os
import mysql.connector
from datetime import datetime
import logging

class MySQLBackup:
    """
    A class to handle MySQL database backups, including structure and data.

    Attributes:
        host (str): MySQL host address.
        user (str): MySQL user name.
        password (str): MySQL user password.
        database (str): Name of the MySQL database to backup.
        backup_dir (str): Directory where backup files will be stored.
        log_dir (str): Directory where log files will be stored.
    """
    def __init__(self, host, user, password, database, backup_dir, log_dir):
        """
        Initialize the MySQLBackup class with connection details and directories.

        :param host: MySQL host address.
        :param user: MySQL user name.
        :param password: MySQL user password.
        :param database: Name of the MySQL database to backup.
        :param backup_dir: Directory where backup files will be stored.
        :param log_dir: Directory where log files will be stored.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.backup_dir = backup_dir
        self.log_dir = log_dir
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()
        self.setup_logging()
        self.ensure_directories_exist()

    def setup_logging(self):
        """
        Set up logging for the backup process.
        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.logger = logging.getLogger('mysql_backup')
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(os.path.join(self.log_dir, 'mysql_backup.log'))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def ensure_directories_exist(self):
        """
        Ensure that the backup and log directories exist.
        """
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def backup_structure(self):
        """
        Backup the structure of the MySQL database (schema only).
        """
        self.logger.info("Starting MySQL structure backup")
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        backup_file = os.path.join(self.backup_dir, f'mysql_structure_{timestamp}.sql')
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        with open(backup_file, 'w') as f:
            for table in tables:
                table_name = table[0]
                self.cursor.execute(f"SHOW CREATE TABLE {table_name}")
                create_table_stmt = self.cursor.fetchone()[1]
                f.write(f"{create_table_stmt};\n")
        self.logger.info(f"MySQL structure backup completed: {backup_file}")

    def backup_data(self):
        """
        Backup the data of the MySQL database (data only).
        """
        self.logger.info("Starting MySQL data backup")
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        backup_file = os.path.join(self.backup_dir, f'mysql_data_{timestamp}.sql')
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        with open(backup_file, 'w') as f:
            for table in tables:
                table_name = table[0]
                self.cursor.execute(f"SELECT * FROM {table_name}")
                rows = self.cursor.fetchall()
                for row in rows:
                    row_data = ', '.join([f"'{str(val)}'" for val in row])
                    f.write(f"INSERT INTO {table_name} VALUES ({row_data});\n")
        self.logger.info(f"MySQL data backup completed: {backup_file}")

    def backup_full(self):
        """
        Backup the full MySQL database (both structure and data).
        """
        self.logger.info("Starting full MySQL backup")
        self.backup_structure()
        self.backup_data()

    def close(self):
        """
        Close the MySQL connection and logger.
        """
        self.cursor.close()
        self.conn.close()
        self.logger.info("MySQL backup connection closed")

def mysql_backup(host, user, password, backup_dir, log_dir, backup_type, database):
    """
    Function to perform MySQL backup based on the specified backup type.

    :param host: MySQL host address.
    :param user: MySQL user name.
    :param password: MySQL user password.
    :param backup_dir: Directory where backup files will be stored.
    :param log_dir: Directory where log files will be stored.
    :param backup_type: Type of backup ('structure', 'data', 'full').
    :param database: Name of the MySQL database to backup.
    """
    backup = MySQLBackup(host, user, password, database, backup_dir, log_dir)
    if backup_type == 'structure':
        backup.backup_structure()
    elif backup_type == 'data':
        backup.backup_data()
    elif backup_type == 'full':
        backup.backup_full()
    backup.close()
