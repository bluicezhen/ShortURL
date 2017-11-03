import json
import os
import tornado.gen
import tornado.web
from lib import n64
from lib.mysql import mysql_pool

if os.path.exists("env_dev"):
    from conf_dev import conf
else:
    from conf import conf

_host = conf["host"]


class HandlerURL_l(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    def options(self):
        self.set_status(200)
        self.finish()

    @tornado.gen.coroutine
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-Type', 'application/json; charset=utf-8')
        try:
            url = json.loads(self.request.body.decode('utf-8'))["url"]
        except KeyError:
            self.send_error(400)
        with (yield mysql_pool.Connection()) as conn:
            try:
                with conn.cursor() as cursor:
                    yield cursor.execute(f"INSERT INTO url (url) VALUES ('{ url }')")
                    yield cursor.execute("SELECT LAST_INSERT_ID()")
                    url_id = cursor.fetchone()[0]
                    self.write(json.dumps({"short_url": _host + n64.encode(url_id)}))
                    yield conn.commit()
            except Exception as e:
                print(e)
                yield conn.rollback()
                self.finish()
