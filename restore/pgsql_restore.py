import os
import psycopg2
import logging

class PgSQLRestore:
    """
    A class to handle PostgreSQL database restoration, including structure, data, and sequences.

    Attributes:
        host (str): PostgreSQL host address.
        user (str): PostgreSQL user name.
        password (str): PostgreSQL user password.
        backup_dir (str): Directory where backup files are stored.
        log_dir (str): Directory where log files are stored.
        database (str): Name of the database to restore.
    """
    def __init__(self, host, user, password, backup_dir, log_dir, database):
        """
        Initialize the PgSQLRestore class with connection details and directories.

        :param host: PostgreSQL host address.
        :param user: PostgreSQL user name.
        :param password: PostgreSQL user password.
        :param backup_dir: Directory where backup files are stored.
        :param log_dir: Directory where log files are stored.
        :param database: Name of the database to restore.
        """
        self.host = host
        self.user = user
        self.password = password
        self.backup_dir = backup_dir
        self.log_dir = log_dir
        self.database = database
        self.setup_logging()
        self.ensure_directories_exist()
        self.create_database_if_not_exists()

        # Connect to the target database
        self.connect_to_database()

    def setup_logging(self):
        """
        Set up logging for the restore process.
        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        formatter = logging.Formatter('%(asctime)s %(levellevel)s %(message)s')
        self.logger = logging.getLogger('pgsql_restore')
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(os.path.join(self.log_dir, 'pgsql_restore.log'))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def ensure_directories_exist(self):
        """
        Ensure that the backup and log directories exist.
        """
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def connect_to_database(self):
        """
        Connect to the PostgreSQL database.
        """
        try:
            self.conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.database)
            self.cursor = self.conn.cursor()
            self.logger.info(f"Connected to PostgreSQL database: {self.database}")
        except psycopg2.Error as e:
            self.logger.error(f"Error connecting to PostgreSQL database: {e}")
            raise

    def create_database_if_not_exists(self):
        """
        Create the PostgreSQL database if it does not already exist.
        """
        try:
            conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname='postgres')
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{self.database}'")
            if cursor.fetchone() is None:
                cursor.execute(f"CREATE DATABASE {self.database}")
                self.logger.info(f"Database {self.database} created.")
            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            self.logger.error(f"Error creating PostgreSQL database: {e}")
            raise

    def restore_sequences(self):
        """
        Restore the sequences of the PostgreSQL database.
        """
        self.logger.info("Starting PostgreSQL sequences restore")
        backup_file = self.get_latest_backup('sequences')
        with open(backup_file, 'r') as f:
            sql_script = f.read()
            sequences_script = self.extract_sequences(sql_script)
            try:
                for sequence in sequences_script.split(';'):
                    if sequence.strip():
                        self.cursor.execute(sequence)
            except psycopg2.errors.SyntaxError as e:
                self.logger.error(f"Error restoring sequences: {e}")
                raise
        self.logger.info(f"PostgreSQL sequences restored from {backup_file}")

    def restore_tables(self):
        """
        Restore the tables of the PostgreSQL database.
        """
        self.logger.info("Starting PostgreSQL tables restore")
        backup_file = self.get_latest_backup('structure')
        with open(backup_file, 'r') as f:
            sql_script = f.read()
            tables_script = self.extract_tables(sql_script)
            try:
                for table in tables_script.split(';'):
                    if table.strip():
                        self.cursor.execute(table)
            except psycopg2.errors.SyntaxError as e:
                self.logger.error(f"Error restoring tables: {e}")
                raise
        self.logger.info(f"PostgreSQL tables restored from {backup_file}")

    def restore_data(self):
        """
        Restore the data of the PostgreSQL database.
        """
        self.logger.info("Starting PostgreSQL data restore")
        backup_file = self.get_latest_backup('data')
        with open(backup_file, 'r') as f:
            sql_script = f.read()
            try:
                for command in sql_script.split(';'):
                    if command.strip():
                        self.cursor.execute(command)
            except psycopg2.errors.SyntaxError as e:
                self.logger.error(f"Error restoring data: {e}")
                raise
        self.logger.info(f"PostgreSQL data restored from {backup_file}")

    def restore_full(self):
        """
        Restore the full PostgreSQL database (both structure and data).
        """
        self.logger.info("Starting full PostgreSQL restore")
        self.restore_sequences()
        self.restore_tables()
        self.restore_data()
        self.logger.info("Full PostgreSQL restore completed")

    def get_latest_backup(self, backup_type):
        """
        Get the latest backup file of the specified type.

        :param backup_type: Type of backup ('sequences', 'structure', 'data').
        :return: Path to the latest backup file.
        :raises FileNotFoundError: If no backup files are found.
        """
        backup_files = [f for f in os.listdir(self.backup_dir) if backup_type in f]
        if not backup_files:
            raise FileNotFoundError(f"No {backup_type} backup files found in {self.backup_dir}")
        latest_backup = max(backup_files, key=lambda f: os.path.getctime(os.path.join(self.backup_dir, f)))
        return os.path.join(self.backup_dir, latest_backup)

    def close(self):
        """
        Close the PostgreSQL connection and logger.
        """
        self.cursor.close()
        self.conn.close()
        self.logger.info("PostgreSQL restore connection closed")

    def extract_sequences(self, sql_script):
        """
        Extract the sequences SQL commands from the script.

        :param sql_script: The full SQL script containing sequences and tables.
        :return: The SQL script with only the sequences.
        """
        sequences_script = ""
        for line in sql_script.splitlines():
            if 'CREATE SEQUENCE' in line or 'ALTER SEQUENCE' in line:
                sequences_script += line + "\n"
        return sequences_script

    def extract_tables(self, sql_script):
        """
        Extract the tables SQL commands from the script.

        :param sql_script: The full SQL script containing sequences and tables.
        :return: The SQL script with only the tables.
        """
        tables_script = ""
        for line in sql_script.splitlines():
            if 'CREATE TABLE' in line or 'INSERT INTO' in line:
                tables_script += line + "\n"
        return tables_script

def pgsql_restore(host, user, password, backup_dir, log_dir, restore_type, database):
    """
    Function to perform PostgreSQL restore based on the specified restore type.

    :param host: PostgreSQL host address.
    :param user: PostgreSQL user name.
    :param password: PostgreSQL user password.
    :param backup_dir: Directory where backup files are stored.
    :param log_dir: Directory where log files are stored.
    :param restore_type: Type of restore ('structure', 'data', 'full').
    :param database: Name of the database to restore.
    """
    restore = PgSQLRestore(host, user, password, backup_dir, log_dir, database)
    if restore_type == 'structure':
        restore.restore_sequences()
        restore.restore_tables()
    elif restore_type == 'data':
        restore.restore_data()
    elif restore_type == 'full':
        restore.restore_full()
    restore.close()
