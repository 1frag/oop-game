import tornado
import tornado.web
from objects import *


class ConflictsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'show_conflicts.html',
            conflicts=list(enumerate(Conflict.objects())),
            colonies=list(enumerate(Colony.objects())),
        )
