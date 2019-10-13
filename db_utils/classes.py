from functools import reduce


class DataBase(dict):
    def __init__(self):
        super(dict, self).__init__()
        self.migrate()

    def migrate(self):
        from .migrations import ops
        for op in ops:
            op(self)

    def get_objects(self, table):
        for key, value in self[table].items():
            if key not in ['id']:
                yield value

    @classmethod
    def get_db(cls, new_db=None, db=[], index=0):
        if new_db:
            return db.append(new_db)
        if not db:
            raise NotImplementedError
        return db[index]


class BaseModel:
    id = None

    @classmethod
    def pre_fun(cls) -> [DataBase, str]:
        db = DataBase.get_db()
        name = cls.__name__
        return db, name

    def save(self):
        db, name = self.pre_fun()
        self.id = db[name]['id']
        db[name][db[name]['id']] = self
        db[name]['id'] += 1
        return self

    @classmethod
    def objects(cls):
        db, name = cls.pre_fun()
        return list(db.get_objects(name))

    @classmethod
    def filter(cls, **kwargs):
        db, name = cls.pre_fun()

        def is_take(obj):
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    if getattr(obj, key) != value:
                        return False
            return True

        return list(filter(is_take, cls.objects()))

    @classmethod
    def values_list(cls, *args, flat=False, **kwargs):
        lst = cls.filter(**kwargs)

        def get_only_values(obj):
            for arg in args:
                if hasattr(obj, arg):
                    yield getattr(obj, arg)

        result = list(map(lambda obj: list(get_only_values(obj)), lst))
        if not result: return []
        if flat:
            return reduce(lambda lst1, lst2: lst1 + lst2, result)
        return result

    def delete(self):
        db, name = self.pre_fun()
        db[name].pop(self.id)
