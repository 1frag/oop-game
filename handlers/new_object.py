import tornado
import tornado.web
import random
import json

from objects import *


class NewObjectHandler(tornado.web.RequestHandler):
    def _new_colony(self):
        name = self.get_body_argument('name')
        chief = self.get_body_argument('chief')

        if name in Colony.values_list('name', flat=True):
            return dict(error='Failed. Input other name')

        war = Warrior(alias=chief, cost=[], force=10,).save()

        col = Colony(name=name, strength=1,
                     resources=self._start_resources).save()
        col.attach_member(war, Role.CHIEF)

        Planet(name=f"planet {name}'s", colony=col).save()

        return dict(name=col.name, war=chief, resources=col.resources)

    def get_related_colony(self):
        name = self.get_body_argument('_colony_name')
        try:
            col = Colony.filter(name=name)[0]
        except Exception as e:
            raise tornado.web.HTTPError(400, reason=e)
        return col

    def _new_planet(self):
        name = self.get_body_argument('name')
        col = self.get_related_colony()
        Planet(name=name, colony=col).save()
        return dict(answer='Created')

    def _new_member(self):
        col: Colony = self.get_related_colony()

        alias = self.get_body_argument('alias')
        role = self.get_body_argument('role')
        force = self.get_body_argument('force')
        role = Role.MEMBER if role == 'Member' else Role.CHIEF

        try:
            cost = random.choice([it for it in col.resources.items() if it[1]])
        except IndexError:
            return dict(
                code=1,
                error='Not enough money',
            )
        else:
            col.resources[cost[0]] -= 1

        war = Warrior(force=force, cost=dict([cost]), alias=alias)
        col.attach_member(war, role=role)
        return {'result': 'Success'}

    def _new_resource(self):
        col = self.get_related_colony()
        res_name = self.get_body_argument('res_name')
        count = self.get_body_argument('count')

        col.resources[res_name] += int(count)
        return {'result': 'Success'}

    @property
    def _start_resources(self):
        return {res.name: random.randrange(10) for res in Resource.objects()}

    def post(self, target):
        target = target.lower()

        def er(): raise NotImplementedError(f'{target} not supported')

        data = {
            'colony': self._new_colony,
            'planet': self._new_planet,
            'member': self._new_member,
            'resource': self._new_resource,
        }.get(target, er)()
        self.write(json.dumps(data))
