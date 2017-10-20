import tormysql
import os.path
if os.path.exists("env_dev"):
    from conf_dev import conf
else:
    from conf import conf

c = conf["mysql"]

mysql_pool = tormysql.ConnectionPool(
    max_connections=20,
    idle_seconds=7200,
    wait_connection_timeout=3,
    host=c["host"],
    user=c["user"],
    passwd=c["password"],
    db=c["db"],
    charset=c["charset"]
)
