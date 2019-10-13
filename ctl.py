from objects import *


class Game:

    def __init__(self):
        self.create_resources()

    @staticmethod
    def create_resources():
        for cost, name in enumerate(['Apple', 'Banana', 'Cherry']):
            Resource(
                name=name,
                cost=cost,
            ).save()
