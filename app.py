from tornado.options import options, define
import tornado
import os
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.locks
import tornado.web
import os.path
import logging

from ctl import Game
from objects import *
from handlers import *
from db_utils.classes import DataBase

define("port", default="8000", help="Listening port", type=str)
define('debug', default=True, help='run in debug mode')


db = DataBase()
DataBase.get_db(new_db=db)
game = Game()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'index.html',
            colonies=list(enumerate(Colony.objects())),
        )


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r'/', MainHandler),
            (r'/new/(?P<target>[^/]*)/', NewObjectHandler),
            (r'/colony/detail/(?P<name>[^/]*)/', DetailColony),
            (r'/colony/remove/(?P<name>[^/]*)/', RemoveColony),
            (r'/conflicts/', ConflictsHandler),
            (r'/conflict/detail/(?P<code>[^/]*)/', DetailConflict),
            (r'/conflict/change/(?P<code>[^/]*)/', ChangeConflict),
            (r'/conflict/resolve/(?P<code>[^/]*)/', ResolveConflict),
        ],
        cookie_secret='p@ssw0rd',
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        xsrf_cookies=True,
        debug=options.debug,
    )

    print("Server listening on port " + str(options.port))
    logging.getLogger().setLevel(logging.DEBUG)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
