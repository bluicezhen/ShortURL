import tornado.gen
import tornado.web
from lib import n64
from lib.mysql import mysql_pool


class HandlerURL(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', ' POST, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    @tornado.gen.coroutine
    def get(self, n_64):
        self.set_header("Access-Control-Allow-Origin", "*")
        with (yield mysql_pool.Connection()) as conn:
            try:
                with conn.cursor() as cursor:
                    yield cursor.execute(f"SELECT url FROM url WHERE id = { n64.decode(n_64) }")
                    url = cursor.fetchone()
                    if url:
                        self.redirect(url[0], permanent=True)
                    else:
                        self.send_error(404)
            except Exception as e:
                print(e)
                yield conn.rollback()
                self.finish()
