# MySQL SSH Query Executor

This Python script allows you to execute multiple SQL queries stored in SQL files against a MySQL database via an SSH tunnel. The script connects to a remote MySQL database through an SSH tunnel and executes SQL queries for specified locations. The locations are passed dynamically to the SQL queries using the `@location` parameter in the SQL files.

The configuration for SSH and MySQL database connection details is stored separately in a JSON configuration file, making it easy to update the connection details without modifying the Python script.

## Features

- **SSH Tunnel**: Establishes a secure SSH tunnel to connect to the remote MySQL database.
- **Dynamic Location Parameter**: Executes SQL queries for different locations by passing the location as a parameter (`@location`) in the SQL queries.
- **Multiple SQL Queries**: Supports executing multiple SQL queries stored in a file.
- **Modular Configuration**: All SSH and database connection details are stored in a separate `config.json` file, allowing easy updates to the connection settings.
- **Error Handling**: Provides basic error handling for SSH, database connection, and SQL query execution.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- `mysql-connector-python` for connecting to MySQL
- `sshtunnel` for establishing an SSH tunnel

You can install the required Python packages using pip:

```bash
pip install mysql-connector-python sshtunnel
