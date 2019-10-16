import tornado
import tornado.web
from objects import *


class ChangeConflict(tornado.web.RequestHandler):
    def get(self, code):
        try:
            conf = Conflict.filter(id=int(code))[0]
        except IndexError:
            self.render('404.html', error='Запрашиваемого конфликта нет')
            return
        self.render(
            'change_conf.html',
            conf=conf,
            inner=self.collect_inner(conf),
            outer=self.collect_outer(conf),
        )

    @staticmethod
    def collect_inner(conf: Conflict):
        return {
            'places': conf.places,
            'participants': conf.participants,
        }

    @staticmethod
    def collect_outer(conf: Conflict):
        places = []
        cleared_pl = []
        cleared_cols = []
        for pa in conf.participants:  # type: Colony
            places.extend(pa.get_related_planets())

        for pl in places:  # type: Planet
            if pl not in conf.places:
                cleared_pl.append(pl)

        for col in Colony.objects():  # type: Colony
            if col not in conf.participants:
                cleared_cols.append(col)

        return {
            'places': cleared_pl,
            'participants': cleared_cols,
        }

    def post(self, code):
        try:
            conf = Conflict.filter(id=int(code))[0]
        except IndexError:
            self.render('404.html', error='Запрашиваемого конфликта нет')
            return
        stage_no = 0
        while True:
            arg = self.get_body_argument(f'st{stage_no}', None)
            if arg is None:
                print(f'from stage{stage_no}')
                break
            stage_no += 1
            side, klass, code = arg.split('$')
            self.move(conf, side, klass, int(code))

        self.write({'result': 'Successful'})

    def check_xsrf_cookie(self) -> None:
        return None

    @staticmethod
    def move(conf: Conflict, side, klass, code):
        print(side, klass, code)
        obj = {
            'places': Planet,
            'participants': Colony,
        }[klass].filter(id=code)[0]

        callback = {
            0: conf.add_participant,
            1: conf.add_place,
            2: conf.remove_participant,
            3: conf.remove_place,
        }[((side == 'to') << 1) + (klass == 'places')]

        callback(obj)
