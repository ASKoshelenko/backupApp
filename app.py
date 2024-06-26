import os
from dotenv import load_dotenv
import click
from backup.mysql_backup import mysql_backup
from backup.pgsql_backup import pgsql_backup
from restore.mysql_restore import mysql_restore
from restore.pgsql_restore import pgsql_restore

# Load environment variables from .env file
load_dotenv()

# MySQL environment variables
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# PostgreSQL environment variables
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')

# Directories for backups and logs
BACKUP_DIR = os.getenv('BACKUP_DIR')
LOG_DIR = os.getenv('LOG_DIR')

# Create directories if they do not exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

@click.group()
def cli():
    """Command line interface group."""
    pass

@cli.command()
@click.option('--dbtype', type=click.Choice(['mysql', 'pgsql']), required=True, help='Type of the database to backup.')
@click.option('--structure', is_flag=True, help='Backup database structure only.')
@click.option('--data', is_flag=True, help='Backup database data only.')
@click.option('--full', is_flag=True, help='Backup full database (structure and data).')
def backup(dbtype, structure, data, full):
    """
    Backup the specified database.

    :param dbtype: The type of database to backup ('mysql' or 'pgsql').
    :param structure: Flag to indicate if only the structure should be backed up.
    :param data: Flag to indicate if only the data should be backed up.
    :param full: Flag to indicate if the full database (structure and data) should be backed up.
    """
    if dbtype == 'mysql':
        if structure:
            mysql_backup(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, BACKUP_DIR, LOG_DIR, 'structure', MYSQL_DATABASE)
        elif data:
            mysql_backup(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, BACKUP_DIR, LOG_DIR, 'data', MYSQL_DATABASE)
        elif full:
            mysql_backup(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, BACKUP_DIR, LOG_DIR, 'full', MYSQL_DATABASE)
    elif dbtype == 'pgsql':
        if structure:
            pgsql_backup(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, BACKUP_DIR, LOG_DIR, 'structure', POSTGRES_DATABASE)
        elif data:
            pgsql_backup(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, BACKUP_DIR, LOG_DIR, 'data', POSTGRES_DATABASE)
        elif full:
            pgsql_backup(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, BACKUP_DIR, LOG_DIR, 'full', POSTGRES_DATABASE)

@cli.command()
@click.option('--dbtype', type=click.Choice(['mysql', 'pgsql']), required=True, help='Type of the database to restore.')
@click.option('--structure', is_flag=True, help='Restore database structure only.')
@click.option('--data', is_flag=True, help='Restore database data only.')
@click.option('--full', is_flag=True, help='Restore full database (structure and data).')
@click.option('--new-database', default=None, help='Name of the new database to restore to.')
def restore(dbtype, structure, data, full, new_database):
    """
    Restore the specified database.

    :param dbtype: The type of database to restore ('mysql' or 'pgsql').
    :param structure: Flag to indicate if only the structure should be restored.
    :param data: Flag to indicate if only the data should be restored.
    :param full: Flag to indicate if the full database (structure and data) should be restored.
    :param new_database: The name of the new database to restore to.
    """
    if dbtype == 'mysql':
        if structure:
            mysql_restore(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, BACKUP_DIR, LOG_DIR, 'structure', new_database)
        elif data:
            mysql_restore(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, BACKUP_DIR, LOG_DIR, 'data', new_database)
        elif full:
            mysql_restore(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, BACKUP_DIR, LOG_DIR, 'full', new_database)
    elif dbtype == 'pgsql':
        if structure:
            pgsql_restore(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, BACKUP_DIR, LOG_DIR, 'structure', new_database if new_database else POSTGRES_DATABASE)
        elif data:
            pgsql_restore(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, BACKUP_DIR, LOG_DIR, 'data', new_database if new_database else POSTGRES_DATABASE)
        elif full:
            pgsql_restore(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, BACKUP_DIR, LOG_DIR, 'full', new_database if new_database else POSTGRES_DATABASE)

if __name__ == '__main__':
    cli()
