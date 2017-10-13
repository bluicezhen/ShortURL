import n64
import os
import tornado.gen
import tornado.ioloop
import tornado.web
from mysql import mysql_pool

_host = "http://localhost/"

io_loop = tornado.ioloop.IOLoop.instance()


class HandlerURL_l(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        url = "http://www.zhen37.me2"
        with (yield mysql_pool.Connection()) as conn:
            try:
                with conn.cursor() as cursor:
                    yield cursor.execute(f"INSERT INTO url (url) VALUES ('{ url }')")
                    url_id = cursor.fetchone()[0]
                    self.write(_host + n64.encode(url_id))
                    yield conn.commit()
            except Exception as e:
                print(e)
                yield conn.rollback()
                self.finish()

    def get(self):
        self.render("template/index.html")


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


def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "debug": True
    }
    return tornado.web.Application([
        ("/([0-9a-zA-Z_-]+)", HandlerURL),
        ("/", HandlerURL_l),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    io_loop.start()
