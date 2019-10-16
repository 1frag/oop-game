from typing import List, Tuple, Union, Dict
from db_utils.classes import BaseModel
from functions import random_alias
from enum import Enum, auto
import attr


class Role(Enum):
    CHIEF = auto()
    MEMBER = auto()


class ConflictStatus(Enum):
    STARTED = auto()
    FINISHED = auto()


@attr.s(hash=True)
class Resource(BaseModel):
    name = attr.ib(type=str)
    cost = attr.ib(type=int)


@attr.s
class Warrior(BaseModel):
    alias = attr.ib(type=str)
    cost = attr.ib(type=Dict[Resource, int])
    force = attr.ib(type=int, default=1)


@attr.s
class Colony(BaseModel):
    name = attr.ib(type=str)
    strength = attr.ib(type=int)
    members = attr.ib(type=List[Tuple[Warrior, Role]])
    resources = attr.ib(type=Dict[Resource, int])

    def attack(self, other):
        conf = Conflict([], [], []).save()
        conf.add_participant(self)
        conf.add_participant(other)
        return conf

    def attach_member(self, warrior: Warrior, role=Role.MEMBER):
        self.members.append((warrior, role))

    def get_related_planets(self):
        return Planet.filter(colony=self)


@attr.s
class Entity(BaseModel):
    from_ = attr.ib(type=Colony)
    to = attr.ib(type=Colony)


@attr.s
class Debt(Entity):
    resource = attr.ib(type=Resource)
    count = attr.ib(type=int)


@attr.s
class Planet(BaseModel):
    name = attr.ib(type=str)
    colony = attr.ib(type=Colony)


@attr.s
class Escape(Entity):
    planet = attr.ib(type=Planet)


@attr.s
class Conflict(BaseModel):
    participants = attr.ib(type=List[Colony])
    places = attr.ib(type=List[Planet])
    result = attr.ib(type=List[Entity])
    alias = attr.ib(type=str, default=None, converter=random_alias)
    status = attr.ib(
        default=ConflictStatus.STARTED,
        type=ConflictStatus
    )

    def add_place(self, place: Planet):
        self.places.append(place)

    def add_to_result(self, debt: Debt):
        self.result.append(debt)

    def set_status(self, status: Union[ConflictStatus, str]):
        if isinstance(status, ConflictStatus):
            self.status = status
        else:
            assert status in ConflictStatus.__members__
            self.status = ConflictStatus.__members__[status]

    def add_participant(self, participant: Colony):
        self.participants.append(participant)

    def remove_participant(self, participant: Colony):
        ind = self.participants.index(participant)
        self.participants.pop(ind)

    def remove_place(self, place: Planet):
        ind = self.places.index(place)
        self.places.pop(ind)
