import psycopg2  # Import the psycopg2 library for PostgreSQL connection
from datetime import datetime


# PostgreSQL connection details
host = "172.21.0.3" 
port = 5432  
user = "postgres"  
password = "1234"  
database = "postgres" 

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
    cursor = conn.cursor()  # Create a cursor object for executing queries

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)
    exit(1)

# Define the table creation query (if it doesn't exist)
create_table_query = """
CREATE TABLE IF NOT EXISTS logspg (
    timestamp TIMESTAMP WITHOUT TIME ZONE,
    user_id INTEGER,
    action VARCHAR(255),
    ad_id VARCHAR(255),
    campaign_id VARCHAR(255),
    platform VARCHAR(255)
);
"""

# Execute the table creation query (ignoring errors if table already exists)
try:
    cursor.execute(create_table_query)
    conn.commit()
except psycopg2.Error:
    conn.rollback()  # Rollback any changes in case of error

# Load data from file
file_path = "/opt/airflow/dags/handle/log/logch.txt"

try:
    with open(file_path, "r") as file:
        for line in file:
            # Parse each line and prepare data for insertion
            data = eval(line.strip())  # Assuming each line is a tuple in string format
            formatted_timestamp = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S").isoformat() # Convert timestamp to ISO format

            # Define the insert query with placeholders for data
            insert_query = """
                INSERT INTO logspg (timestamp, user_id, action, ad_id, campaign_id, platform)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            # Execute the insert query with the parsed data
            cursor.execute(insert_query, (formatted_timestamp, data[1], data[2], data[3], data[4], data[5]))
            conn.commit()

    print("\nLogs inserted successfully into PostgreSQL!\n")

except (Exception, psycopg2.Error) as error:
    print(f"Error inserting data into PostgreSQL: {error}")
    conn.rollback()  # Rollback any changes in case of error

# Close the connection
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
