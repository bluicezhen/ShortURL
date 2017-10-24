import os
import tornado.gen
import tornado.ioloop
import tornado.web
from handler import HandlerURL, HandlerURL_l

if os.path.exists("env_dev"):
    from conf_dev import conf
else:
    from conf import conf
io_loop = tornado.ioloop.IOLoop.instance()


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
    app.listen(conf["listen"], address="0.0.0.0")
    io_loop.start()
