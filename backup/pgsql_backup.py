import os
import psycopg2
from datetime import datetime
import logging

class PgSQLBackup:
    """
    A class to handle PostgreSQL database backups, including structure and data.

    Attributes:
        host (str): PostgreSQL host address.
        user (str): PostgreSQL user name.
        password (str): PostgreSQL user password.
        database (str): Name of the PostgreSQL database to backup.
        backup_dir (str): Directory where backup files will be stored.
        log_dir (str): Directory where log files will be stored.
    """
    def __init__(self, host, user, password, database, backup_dir, log_dir):
        """
        Initialize the PgSQLBackup class with connection details and directories.

        :param host: PostgreSQL host address.
        :param user: PostgreSQL user name.
        :param password: PostgreSQL user password.
        :param database: Name of the PostgreSQL database to backup.
        :param backup_dir: Directory where backup files will be stored.
        :param log_dir: Directory where log files will be stored.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.backup_dir = backup_dir
        self.log_dir = log_dir
        self.conn = psycopg2.connect(host=host, user=user, password=password, dbname=database)
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
        self.logger = logging.getLogger('pgsql_backup')
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(os.path.join(self.log_dir, 'pgsql_backup.log'))
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
        Backup the structure of the PostgreSQL database (schema only).
        """
        self.logger.info("Starting PostgreSQL structure backup")
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        backup_file = os.path.join(self.backup_dir, f'pgsql_structure_{timestamp}.sql')
        with open(backup_file, 'w') as f:
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = self.cursor.fetchall()
            for table in tables:
                table = table[0]
                self.cursor.execute(f"SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = '{table}'")
                columns = self.cursor.fetchall()
                ddl = f"CREATE TABLE {table} (\n"
                ddl += ",\n".join([f"{col[0]} {col[1]} {'' if col[2] == 'YES' else 'NOT NULL'} {'' if not col[3] else f'DEFAULT {col[3]}'}" for col in columns])
                ddl += "\n);\n"
                f.write(ddl)
        self.logger.info(f"PostgreSQL structure backup completed: {backup_file}")

    def backup_data(self):
        """
        Backup the data of the PostgreSQL database (data only).
        """
        self.logger.info("Starting PostgreSQL data backup")
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        backup_file = os.path.join(self.backup_dir, f'pgsql_data_{timestamp}.sql')
        with open(backup_file, 'w') as f:
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = self.cursor.fetchall()
            for table in tables:
                table = table[0]
                self.cursor.execute(f"SELECT * FROM {table}")
                rows = self.cursor.fetchall()
                for row in rows:
                    formatted_row = ", ".join([f"'{str(value)}'" if isinstance(value, str) else str(value) for value in row])
                    f.write(f"INSERT INTO {table} VALUES ({formatted_row});\n")
        self.logger.info(f"PostgreSQL data backup completed: {backup_file}")

    def backup_full(self):
        """
        Backup the full PostgreSQL database (both structure and data).
        """
        self.logger.info("Starting full PostgreSQL backup")
        self.backup_structure()
        self.backup_data()

    def close(self):
        """
        Close the PostgreSQL connection and logger.
        """
        self.cursor.close()
        self.conn.close()
        self.logger.info("PostgreSQL backup connection closed")

def pgsql_backup(host, user, password, backup_dir, log_dir, backup_type, database):
    """
    Function to perform PostgreSQL backup based on the specified backup type.

    :param host: PostgreSQL host address.
    :param user: PostgreSQL user name.
    :param password: PostgreSQL user password.
    :param backup_dir: Directory where backup files will be stored.
    :param log_dir: Directory where log files will be stored.
    :param backup_type: Type of backup ('structure', 'data', 'full').
    :param database: Name of the PostgreSQL database to backup.
    """
    backup = PgSQLBackup(host, user, password, database, backup_dir, log_dir)
    if backup_type == 'structure':
        backup.backup_structure()
    elif backup_type == 'data':
        backup.backup_data()
    elif backup_type == 'full':
        backup.backup_full()
    backup.close()
