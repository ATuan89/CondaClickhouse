import psycopg2  # Import psycopg2 for PostgreSQL connection
from clickhouse_driver import Client
from clickhouse_driver import errors
from datetime import datetime

# PostgreSQL connection details
source_host = "172.21.0.3"
source_port = 5432  # Default PostgreSQL port
source_user = "postgres"
source_password = "1234"
source_database = "postgres"
source_table = "logspg"  # Replace with your PostgreSQL table name

# ClickHouse connection details
destination_host = "172.21.0.2"
destination_port = 9000  # Default ClickHouse port
destination_user = "default"
destination_password = ""
destination_database = "default"
destination_table = "logdch"  # Replace with your ClickHouse table name

# Connect to PostgreSQL
try:
    source_conn = psycopg2.connect(host=source_host, port=source_port, user=source_user, password=source_password, database=source_database)
    source_cursor = source_conn.cursor()  # Create a cursor for PostgreSQL

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)
    exit(1)

# Connect to ClickHouse
destination_client = Client(host=destination_host, port=destination_port, user=destination_user, password=destination_password, database=destination_database)

try:
    destination_client.execute(
        """
        CREATE TABLE IF NOT EXISTS logdch (
            timestamp DateTime,
            user_id UInt32,
            action String,
            ad_id String,
            campaign_id String,
            platform String
        ) ENGINE = MergeTree ORDER BY (timestamp)
        """
    )
except errors.ServerException as e:
    print(f"Error creating table: {e}")
    exit(1)

# Query data from PostgreSQL table
select_query = f"SELECT * FROM {source_table}"

try:
    # Fetch data from PostgreSQL
    source_cursor.execute(select_query)
    source_data = source_cursor.fetchall()  # Fetch all rows

    # Insert data into ClickHouse table
    for row in source_data:
        row = list(row)
        row[0] = row[0].strftime("%Y-%m-%d %H:%M:%S") # Convert timestamp to string
        insert_query = f"INSERT INTO {destination_table} VALUES {tuple(row)}"
        destination_client.execute(insert_query)

    print("\nData inserted successfully!\n")

except (Exception, errors.Error, psycopg2.Error) as e:
    print(f"Error: {e}")

# Close connections
finally:
    if source_cursor:
        source_cursor.close()
    if source_conn:
        source_conn.close()
    destination_client.disconnect()
