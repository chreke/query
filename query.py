
class Col:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Eq:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Query:
    def __init__(self, table):
        self.tables = [table]
        self.projections = []
        self.selections = []

    def select(self, cols):
        self.projections = cols

    def where(self, op):
        self.selections.append(op)

    def join(self, table):
        self.tables.append(table)


def _to_sql(term):
    match term:
        case int():
            return str(term)
        case str():
            return f"'{term}'"
        case Col(name=name):
            return name
        case Eq(a=a, b=b):
            return _to_sql(a) + " = " + _to_sql(b)
        case other:
            raise Exception(f"Unexpected operator: {other}")
        

def sql(query):
    projections = ", ".join(query.projections) if query.projections else "*"
    tables = ", ".join(query.tables)
    selections = " AND ".join(_to_sql(s) for s in query.selections)
    where = f"WHERE {selections}" if selections else ""
    return f"SELECT ({projections}) FROM {tables} {where}".strip()
