from clickhouse_driver import Client

host = 'localhost'
port = 9000
database = 'default'
user = 'default'
password = ''

client = Client(host=host, port=port, database=database, user=user, password=password)

query = """
    SELECT
    campaign_id,
    count(action) AS total_actions,
    toDate(timestamp) AS date
    FROM
        logd
    GROUP BY
        date,
        campaign_id
    ORDER BY
        date,
        campaign_id;
"""

result = client.execute(query)


print("\nTổng lượng view và click theo Campaign_ID trong một ngày\n")
for row in result:
    print(row)

client.disconnect()

