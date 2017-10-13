import tormysql

mysql_pool = tormysql.ConnectionPool(
    max_connections=20,
    idle_seconds=7200,
    wait_connection_timeout=3,
    host="localhost",
    user="root",
    passwd="123456",
    db="123",
    charset="utf8"
)
