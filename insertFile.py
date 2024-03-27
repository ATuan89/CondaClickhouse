from clickhouse_driver import Client
from clickhouse_driver import errors
from datetime import datetime

# ClickHouse connection details
host = "localhost"  # Replace with your ClickHouse server host
port = 9000  # Replace with your ClickHouse server port
user = "default"  # Replace with your ClickHouse username
password = ""  # Replace with your ClickHouse password
database = "default"  # Replace with your database name (optional)

# Connect to ClickHouse
client = Client(host=host, port=port, user=user, password=password, database=database)

# Create the table (if it doesn't exist)
try:
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
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

# Load data from file
file_path = "./log/logch.txt"

try:
    with open(file_path, "r") as file:
        for line in file:
            # Parse each line and insert into ClickHouse
            data = eval(line.strip())  # Assuming each line is a tuple in string format
            formatted_timestamp = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
            insert_query = """
                INSERT INTO logs (timestamp, user_id, action, ad_id, campaign_id, platform)
                VALUES ('{}', {}, '{}', '{}', '{}', '{}')
            """.format(formatted_timestamp, data[1], data[2], data[3], data[4], data[5])
            client.execute(insert_query)
    print("Logs inserted successfully!")
except errors.Error as e:
    print(f"Error inserting data: {e}")

# Close the connection
client.disconnect()
