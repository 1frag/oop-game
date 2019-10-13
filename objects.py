from typing import List, Tuple, Union, Dict
from db_utils.classes import BaseModel
from random import randrange
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
    members = attr.ib(default=[], type=List[Tuple[Warrior, Role]])
    resources = attr.ib(default={}, type=Dict[Resource, int])

    def attack(self, other):
        Conflict(
            participants=[self, other],
            status=ConflictStatus.STARTED,
            result=[],
        )

    def attach_member(self, warrior: Warrior, role=Role.MEMBER):
        self.members.append((warrior, role))


@attr.s
class Debt(BaseModel):
    from_ = attr.ib(type=Colony)
    to = attr.ib(type=Colony)
    resource = attr.ib(type=Resource)
    count = attr.ib(type=int)


@attr.s
class Planet(BaseModel):
    name = attr.ib(type=str)
    colony = attr.ib(type=Colony)


@attr.s
class Escape(BaseModel):
    from_ = attr.ib(type=Colony)
    to = attr.ib(type=Colony)
    planet = attr.ib(type=Planet)


@attr.s
class Conflict(BaseModel):
    id = attr.ib(type=int, default=randrange(1000000000))
    participants = attr.ib(type=List[Colony], default=[])
    status = attr.ib(
        default=ConflictStatus.STARTED,
        type=ConflictStatus
    )
    places = attr.ib(type=List[Planet], default=[])
    result = attr.ib(type=List[Union[Debt, Escape]], default=[])  # todo:

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
