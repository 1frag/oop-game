import tornado
import tornado.web

from objects import *


class DetailColony(tornado.web.RequestHandler):
    def get(self, name):
        names = Colony.values_list('name', flat=True)
        count = names.count(name)

        if count != 1:
            self.render('colony_detail.html', error=f'find {count}, but expected 1')
            return

        col = Colony.filter(name=name)[0]
        planets = [
            pl.name
            for pl in Planet.objects()
            if pl.colony == col
        ]
        confs = [
            conf.id
            for conf in Conflict.objects()
            if col in conf.participants
        ]
        self.render(
            'colony_detail.html',
            name=name,
            planets=planets,
            resources=col.resources,
            confs=confs,
            members=col.members,
            all_resources=Resource.values_list('name', flat=True),
            error=False,
        )
