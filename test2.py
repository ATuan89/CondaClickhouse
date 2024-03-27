from clickhouse_driver import Client

# Replace with your ClickHouse connection details
host = 'localhost'
port = 9000
database = 'default'
user = 'default'
password = ''

# Connect to ClickHouse
client = Client(host=host, port=port, database=database, user=user, password=password)

# Sample query (replace with your desired query)
query = "SELECT * FROM user LIMIT 10"

# Execute the query
result = client.execute(query)

# Print the results (modify this for your use case)
for row in result:
    print(row)

# Close the connection (optional)
client.disconnect()
