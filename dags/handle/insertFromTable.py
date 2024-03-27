from clickhouse_driver import Client
from clickhouse_driver import errors
from datetime import datetime

# ClickHouse connection details
source_host = "172.21.0.2"
source_port = 9000
source_user = "default"
source_password = ""
source_database = "default"
source_table = "logs"

destination_host = "172.21.0.2"
destination_port = 9000
destination_user = "default"
destination_password = ""
destination_database = "default"
destination_table = "logd"

# Connect to ClickHouse for source table
source_client = Client(host=source_host, port=source_port, user=source_user, password=source_password, database=source_database)

# Connect to ClickHouse for destination table
destination_client = Client(host=destination_host, port=destination_port, user=destination_user, password=destination_password, database=destination_database)

try:
    destination_client.execute(
        """
        CREATE TABLE IF NOT EXISTS logd (
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

# Query data from source table
select_query = f"SELECT * FROM {source_table}"

try:
    # Fetch data from source table
    source_data = source_client.execute(select_query)

    # Insert data into destination table
    for row in source_data:
        # Convert timestamp string to datetime object
        row = list(row)
        row[0] = row[0].strftime("%Y-%m-%d %H:%M:%S")
        # Insert data into destination table
        insert_query = f"INSERT INTO {destination_table} VALUES {tuple(row)}"
        destination_client.execute(insert_query)

    print("Data inserted successfully!")

except errors.Error as e:
    print(f"Error: {e}")

# Close the connections
source_client.disconnect()
destination_client.disconnect()
