# Relational Algebra DSL

This is a proof-of-concept for a DSL based on relational algebra, as seen in this presentation: <https://www.youtube.com/watch?v=SKXEppEZp9M>

# Usage

The `Query` class represents a [relational algebra][relalg] program. You can initialize it like this:

```python
from query import *

# You need to provide a table name when constructing a query:
query = Query("movies")
```

The `Query` class has the following methods:

- `Query.join(table)` Joins a table to the current query
- `Query.where(ops)` Filters rows based on the given predicate
- `Query.select(cols)` Removes everything but the given columns from the result

To filter queries, the following operators are available in the `query` module:

- `Col(name)` References a column
- `Eq(a, b)` Compares two expressions for equality
- `Gt(a, b)` Checks whether `a` is greater than `b`
- `Lt(a, b)` Checks whether `a` is lesser than `b`

The `query` module also defines a `sql` function that converts a `Query` to SQL.

# Examples

These examples assume that we have two tables with the following structure:

movies:

- Id
- Director
- Title
- Year

genres:

- MovieId (foreign key to movies.Id)
- Genre

Get all movie titles directed by Ingmar Bergman:

```python
from query import *
q = Query("movies")\
  .where(Eq(Col("Director"), "Ingmar Bergman"))\
  .select(["Title"])
sql(q)
# "SELECT Title FROM movies WHERE Director = 'Ingmar Bergman'"
```

Get all movies directed by Ingmar Bergman after 1960:

```python
q = Query("movies")\
  .where(Eq(Col("Director"), "Ingmar Bergman"))\
  .where(Gt(Col("Year"), 1960))
sql(q)
# "SELECT * FROM movies WHERE Director = 'Ingmar Bergman' AND Year > 1960"
```

Get all the genres that Ingmar Bergman worked in:

```python
q = Query("movies")\
  .where(Eq(Col("Director"), "Ingmar Bergman"))\
  .join("genres")\
  .where(Eq(Col("MovieId"), Col("Id")))
sql(q)
# "SELECT * FROM movies, genres WHERE Director = 'Ingmar Bergman' AND MovieId = Id"
```

[relalg]: https://en.wikipedia.org/wiki/Relational_algebra
