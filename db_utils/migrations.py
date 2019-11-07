def init_table(db):
    tables = ['Colony', 'Planet', 'Warrior', 'Conflict',
              'Resource', 'Debt', 'Escape', 'Builder']
    for table in tables:
        db[table] = dict()
        db[table]['id'] = 1


ops = [
    init_table,
]
