from clickhouse_driver import Client

host = '172.21.0.2'
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
        logs
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

