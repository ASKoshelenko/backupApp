import argparse
from src.backup import backup_mysql, backup_postgresql

def main():
    parser = argparse.ArgumentParser(description="Database Backup Tool")
    parser.add_argument("db_type", choices=['mysql', 'postgresql'], help="Type of database to backup")
    parser.add_argument("db_name", help="Name of the database")
    args = parser.parse_args()

    if args.db_type == 'mysql':
        backup_mysql(args.db_name)
    elif args.db_type == 'postgresql':
        backup_postgresql(args.db_name)

if __name__ == '__main__':
    main()