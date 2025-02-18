import sqlite3
import itertools

class Col:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class BinaryOp:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Eq(BinaryOp):
    pass

class Gt(BinaryOp):
    pass

class Lt(BinaryOp):
    pass


class Query:
    def __init__(self, table):
        self.tables = [table]
        self.projections = []
        self.selections = []

    def select(self, cols):
        self.projections = cols
        return self

    def where(self, op):
        self.selections.append(op)
        return self

    def join(self, table):
        self.tables.append(table)
        return self

    def __str__(self):
        return (
            f"Tables: {self.tables}\n"
            f"Projections: {self.projections}\n"
            f"Selections: {self.selections}\n")


def _to_sql(term):
    match term:
        case Col(name=name):
            return name
        case Eq(a=a, b=b):
            return _to_sql(a) + " = " + _to_sql(b)
        case Gt(a=a, b=b):
            return _to_sql(a) + " > " + _to_sql(b)
        case Lt(a=a, b=b):
            return _to_sql(a) + " < " + _to_sql(b)
        case str():
            return f"'{term}'"
        case int():
            return str(term)
        case _:
            raise Exception(f"Unexpected {term}")
        

def sql(query):
    projections = ", ".join(query.projections) if query.projections else "*"
    tables = ", ".join(query.tables)
    selections = " AND ".join(_to_sql(s) for s in query.selections)
    where = f"WHERE {selections}" if selections else ""
    return f"SELECT {projections} FROM {tables} {where}".strip()


## ADAPTERS

def merge_dicts(dicts):
    merged = {}
    for d in dicts:
        merged.update(d)
    return merged

class Memory:
    def __init__(self, data):
        self.data = data

    @classmethod
    def _compute(cls, term, row):
        match term:
            case Col(name=name):
                return row[name]
            case Eq(a=a, b=b):
                return cls._compute(a, row) == cls._compute(b, row)
            case Gt(a=a, b=b):
                return cls._compute(a, row) > cls._compute(b, row)
            case Lt(a=a, b=b):
                return cls._compute(a, row) < cls._compute(b, row)
            case other:
                return other

    @classmethod
    def _check_row(cls, row, selections):
        return all(cls._compute(s, row) for s in selections)

    @classmethod
    def _project(cls, row, projections):
        if not projections:
            return row.values()
        return [row[p] for p in projections]

    def run(self, query):
        tables = [self.data[t] for t in query.tables]
        rows = (merge_dicts(t) for t in itertools.product(*tables))
        return [
            self._project(r, query.peojections)
            for r in rows
            if self._check_row(r, query.selections)
        ]

class SQLite:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)

    def run(self, query):
        cursor = self.connection.cursor()
        result = cursor.execute(query)
        return result.fetchall()
