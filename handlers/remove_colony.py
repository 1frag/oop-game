import tornado.web
import json

from objects import *


class RemoveColony(tornado.web.RequestHandler):
    def post(self, name):
        col: Colony = Colony.filter(name=name)[0]
        for war, _ in col.members:
            war.delete()
        col.delete()
        self.write(json.dumps({'result': 'success'}))

    def check_xsrf_cookie(self) -> None:
        return None
