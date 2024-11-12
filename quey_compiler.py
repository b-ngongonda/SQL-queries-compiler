import mysql.connector
from sshtunnel import SSHTunnelForwarder
import json
import os


# Function to load configuration from a JSON file
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)


# Function to read SQL query from a file and split into individual queries
def read_sql_from_file(file_path):
    with open(file_path, 'r') as file:
        sql_query = file.read().strip()  # Read and remove any trailing whitespaces
    # Split queries by semicolon, ensuring that empty queries are not included
    queries = [query.strip() for query in sql_query.split(';') if query.strip()]
    return queries


# Function to execute SQL queries from a file for a given location and server configuration
def execute_sql_from_file(sql_file_path, locations, server_config):
    print(f"Running SQL from file: {sql_file_path} on server: {server_config['database']['host']}")

    # Read and split the SQL queries from the file
    queries = read_sql_from_file(sql_file_path)

    # Set up the SSH tunnel and execute the queries for the given locations
    with SSHTunnelForwarder(
            (server_config['ssh']['host'], server_config['ssh']['port']),
            ssh_username=server_config['ssh']['user'],
            ssh_password=server_config['ssh']['password'],
            remote_bind_address=(server_config['database']['host'], server_config['database']['port'])
    ) as tunnel:

        # Establish a connection to the database via the SSH tunnel
        try:
            connection = mysql.connector.connect(
                host='127.0.0.1',
                port=tunnel.local_bind_port,
                user=server_config['database']['user'],
                password=server_config['database']['password'],
                database=server_config['database']['name']
            )

            cursor = connection.cursor()

            # Loop through each location and execute the queries
            for location in locations:
                print(f"\n--- Results for location: {location} ---")
                # For each location, execute all queries in the SQL file
                for query in queries:
                    try:
                        # First, set the @location variable for the current location
                        cursor.execute(f"SET @location = '{location}';")

                        # Execute the current SQL query
                        cursor.execute(query)

                        # Fetch and print the results for SELECT queries
                        if query.strip().upper().startswith('SELECT'):
                            results = cursor.fetchall()
                            if results:
                                for row in results:
                                    print(row)
                            else:
                                print(f"No results returned for location '{location}' from query: {query}")
                        #else:
                            #print(f"Executed query for location '{location}': {query}")

                    except mysql.connector.Error as err:
                        print(f"Error executing query for location '{location}': {err}")

        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


# Load the server configuration from the config file
config_file = 'config.json'  # Path to the JSON configuration file
if not os.path.exists(config_file):
    print(f"Configuration file {config_file} not found!")
else:
    server_config = load_config(config_file)

    # List of SQL files to run
    sql_files = ['active in care.sql']  # Add your SQL file paths here


    # List of locations to get data for i.e. Upper Neno facilities
    locations = ['Dambe clinic','Ligowe HC','Luwani RHC','Magaleta HC','Matandani Rural Health Center','Neno District Hospital', 'Neno Mission HC','Nsambe HC']  # Add your locations here


    # Loop through each SQL file and execute queries for each location
    for sql_file in sql_files:
        if os.path.exists(sql_file):  # Ensure the file exists
            execute_sql_from_file(sql_file, locations, server_config)
        else:
            print(f"SQL file not found: {sql_file}")
