import tornado.gen
import tornado.ioloop
import tornado.web
import tormysql
import n64

_host = "http://localhost/"

mysql_pool = tormysql.ConnectionPool(
    max_connections=20,  # max open connections
    idle_seconds=7200,  # conntion idle timeout time, 0 is not timeout
    wait_connection_timeout=3,  # wait connection timeout
    host="localhost",
    user="root",
    passwd="123456",
    db="123",
    charset="utf8"
)

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
        self.redirect("https://www.baidu.com", permanent=True)


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
    return tornado.web.Application([
        ("/([0-9a-zA-Z_-]+)", HandlerURL),
        ("/", HandlerURL_l),

    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    io_loop.start()
