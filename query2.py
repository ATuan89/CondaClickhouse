from clickhouse_driver import Client

host = 'localhost'
port = 9000
database = 'default'
user = 'default'
password = ''

client = Client(host=host, port=port, database=database, user=user, password=password)

query = """
    SELECT
    user_id,
    countIf(action = 'view') AS views,
    countIf(action = 'click') AS clicks,
    toDate(timestamp) AS date
    FROM
        logd
    GROUP BY
        user_id,
        date;
"""

result = client.execute(query)

print("\nLấy user_id và tổng action theo view và click trong một ngày\n")
for row in result:
    print(row)


client.disconnect()

