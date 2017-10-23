import tornado.gen
import tornado.web
from lib import n64
from lib.mysql import mysql_pool


class HandlerURL(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, n_64):
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
