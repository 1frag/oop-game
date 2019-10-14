import tornado
import tornado.web
from objects import *


class DetailConflict(tornado.web.RequestHandler):
    def get(self, code):
        try:
            cur_conf: Conflict = Conflict.filter(id=int(code))[0]
        except IndexError:
            return self.render(
                '404.html',
                error='По такому айдишнику нет конфликтов',
            )
        self.render(
            'conf_detail.html',
            participants=cur_conf.participants,
            planets=cur_conf.places,
            result=cur_conf.result,
            alias=cur_conf.alias,
            status=cur_conf.status,
        )
