import json
import os
import tornado.gen
import tornado.web
from hashlib import md5
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
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    def options(self):
        self.set_status(200)
        self.finish()

    @tornado.gen.coroutine
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-Type', 'application/json; charset=utf-8')

        try:
            url = json.loads(self.request.body.decode('utf-8'))["url"]  # type:str
            url_md5 = md5("1".encode("utf-8")).hexdigest()
        except KeyError:
            self.send_error(400)
            return

        with (yield mysql_pool.Connection()) as conn:
            try:
                with conn.cursor() as cursor:
                    # Check is user input url in database.
                    yield cursor.execute(f"SELECT id, url FROM url WHERE md5 = \"{ url_md5 }\"")
                    db_url_list = cursor.fetchall()
                    for db_url in db_url_list:
                        _id = db_url[0]  # type: int
                        _url = db_url[1]  # type: str
                        if url == _url:
                            self.write(json.dumps({"short_url": _host + n64.encode(_id)}))
                            return

                    yield cursor.execute(f"INSERT INTO url (url, md5) VALUES ('{ url }', '{ url_md5 }')")
                    yield cursor.execute("SELECT LAST_INSERT_ID()")
                    url_id = cursor.fetchone()[0]
                    self.write(json.dumps({"short_url": _host + n64.encode(url_id)}))
                    yield conn.commit()
            except Exception as e:
                print(e)
                yield conn.rollback()
                self.finish()
