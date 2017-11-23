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
            url_id = n64.decode(n_64)
            client_ip = self.request.remote_ip
            try:
                with conn.cursor() as cursor:
                    # find url
                    yield cursor.execute(f"SELECT url FROM url WHERE id = { url_id }")
                    url = cursor.fetchone()
                    if url:
                        # Add url.visits
                        yield cursor.execute(f"UPDATE url SET visits = visits + 1 WHERE id = { url_id }")
                        yield cursor.execute(f"INSERT INTO record (url_id, client_ip) "
                                             f"VALUES ({ url_id }, '{ client_ip }')")
                        yield conn.commit()
                        self.redirect(url[0], permanent=True)
                    else:
                        self.send_error(404)
            except Exception as e:
                print(e)
                yield conn.rollback()
                self.finish()
