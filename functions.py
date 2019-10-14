from random import choice


def random_alias(spam=None):
    what = ['Война', 'Битва', 'Схватка', 'Междуусобица', 'Сражение']
    op = [('между', 'ами'), ('среди', 'ов'), ('из', 'ов')]
    who = ['интерфейс', 'объект', 'класс', 'наследник']
    sample = '{data[0]} {data[1][0]} {data[2]}{data[1][1]}'
    return sample.format(data=list(map(choice, [what, op, who])))
