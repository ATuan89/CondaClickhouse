from clickhouse_driver import Client
from clickhouse_driver import errors
from datetime import datetime

# ClickHouse connection details
host = "localhost"  # Replace with your ClickHouse server host
port = 9000  # Replace with your ClickHouse server port
user = "default"  # Replace with your ClickHouse username
password = ""  # Replace with your ClickHouse password
database = "default"  # Replace with your database name (optional)

# Log data
log_data = [
    ('2024-03-25 08:30:00', 12345, 'click', 'ad123', 'campaign_xyz', 'Google Ads'),
    # Add more log data tuples here if needed
]

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

# Insert the log data
formatted_log_data = []
for timestamp, user_id, action, ad_id, campaign_id, platform in log_data:
    formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    formatted_log_data.append((formatted_timestamp, user_id, action, ad_id, campaign_id, platform))

try:
    client.execute(
        """
        INSERT INTO logs (timestamp, user_id, action, ad_id, campaign_id, platform)
        VALUES
        """
        + ",".join(["('{}', {}, '{}', '{}', '{}', '{}')".format(*row) for row in formatted_log_data])
    )
    print("Logs inserted successfully!")
except errors.Error as e:
    print(f"Error inserting data: {e}")

# Close the connection
client.disconnect()
