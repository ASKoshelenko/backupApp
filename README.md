
# BackupApp

BackupApp is a utility for backing up and restoring MySQL and PostgreSQL databases. This project includes functionalities for full, structure-only, and data-only backups and restorations.

## Features

- Backup MySQL and PostgreSQL databases.
- Restore MySQL and PostgreSQL databases.
- Support for full, structure-only, and data-only backups.
- Command-line interface using Click.
- Unit tests for connection, backup, and restore functionalities.

## Requirements

- Python 3.9+
- Click
- PyMySQL
- psycopg2-binary
- python-dotenv
- cryptography
- mysql-connector-python

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:ASKoshelenko/backupApp.git
   cd backupApp
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following content:
   ```env
   MYSQL_HOST=your_mysql_host
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=your_mysql_database
   POSTGRES_HOST=your_postgres_host
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DATABASE=your_postgres_database
   BACKUP_DIR=path_to_backup_directory
   LOG_DIR=path_to_log_directory
   ```

## Usage

### Backup

- Full backup:
  ```bash
  python app.py backup --dbtype mysql --full
  python app.py backup --dbtype pgsql --full
  ```

- Structure-only backup:
  ```bash
  python app.py backup --dbtype mysql --structure
  python app.py backup --dbtype pgsql --structure
  ```

- Data-only backup:
  ```bash
  python app.py backup --dbtype mysql --data
  python app.py backup --dbtype pgsql --data
  ```

### Restore

- Full restore:
  ```bash
  python app.py restore --dbtype mysql --full --new-database new_database_name
  python app.py restore --dbtype pgsql --full --new-database new_database_name
  ```

- Structure-only restore:
  ```bash
  python app.py restore --dbtype mysql --structure --new-database new_database_name
  python app.py restore --dbtype pgsql --structure --new-database new_database_name
  ```

- Data-only restore:
  ```bash
  python app.py restore --dbtype mysql --data --new-database new_database_name
  python app.py restore --dbtype pgsql --data --new-database new_database_name
  ```

## Running Tests

To run the unit tests:
```bash
pytest
```

## License

This project is licensed under the MIT License.
