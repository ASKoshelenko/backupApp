import os
import pymysql
import psycopg2

# Configuration variables
MYSQL_HOST = '192.168.194.28'
MYSQL_USER = 'db'
MYSQL_PASSWORD = 'epam'
POSTGRES_HOST = '192.168.194.28'
POSTGRES_USER = 'db'
POSTGRES_PASSWORD = 'epam'
MYSQL_OUTPUT_DIR = '/Users/ask/PycharmProjects/m2-Python-Task-02/backups/mysql'
POSTGRES_OUTPUT_DIR = '/Users/ask/PycharmProjects/m2-Python-Task-02/backups/postgresql'

def escape_quotes(value):
    """Escape single quotes in a SQL value."""
    if value is None:
        return 'NULL'
    return "'" + str(value).replace("'", "''") + "'"

def backup_mysql(db_name):
    """Function to backup MySQL database."""
    connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=db_name)
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        with open(os.path.join(MYSQL_OUTPUT_DIR, f"{table_name}.sql"), 'w') as f:
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`;")
            create_table_stmt = cursor.fetchone()[1]
            f.write(f"{create_table_stmt};\n\n")
            cursor.execute(f"SELECT * FROM `{table_name}`;")
            rows = cursor.fetchall()
            col_names = ", ".join([desc[0] for desc in cursor.description])
            for row in rows:
                values = ", ".join([escape_quotes(x) for x in row])
                f.write(f"INSERT INTO `{table_name}` ({col_names}) VALUES ({values});\n")
    cursor.close()
    connection.close()

def backup_postgresql(db_name):
    """Function to backup PostgreSQL database."""
    connection = psycopg2.connect(host=POSTGRES_HOST, dbname=db_name, user=POSTGRES_USER, password=POSTGRES_PASSWORD)
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        with open(os.path.join(POSTGRES_OUTPUT_DIR, f"{table_name}.sql"), 'w') as f:
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}'")
            column_names = [row[0] for row in cursor.fetchall()]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                values = ", ".join([escape_quotes(x) for x in row])
                f.write(f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({values});\n")
    cursor.close()
    connection.close()