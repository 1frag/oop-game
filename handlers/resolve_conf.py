import tornado.web
import json
from typing import Optional

from objects import *


class ResolveConflict(tornado.web.RequestHandler):
    def post(self, code):
        conf = self.get_conf(code)
        print(self.get_body_argument('data'))

    def get_conf(self, code) -> Optional[Conflict]:
        try:
            conf: Conflict = Conflict.filter(id=int(code))[0]
            return conf
        except IndexError:
            self.render(
                '404.html',
                error='По такому айдишнику нет конфликтов',
            )

    def get(self, code):
        conf = self.get_conf(code)
        self.render(
            'resolve_conf.html',
            conf=conf,
            colonies=conf.participants,
            planets=list(map(lambda pl: [pl.name, pl.colony.name], conf.places)),
            resources=list(map(lambda res: res.name, Resource.objects())),
        )

    def check_xsrf_cookie(self) -> None:
        return None
