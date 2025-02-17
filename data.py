import csv

def load(filename):
    movies = []
    genres = []
    with open(filename, newline='') as f:
        movie_id = 1
        genre_id = 1
        for row in csv.DictReader(f):
            movies.append({
                "Id": movie_id,
                "Title": row["Title"],
                "Director": row["Director"],
                "Year": int(row["Year"]),
                "IMDB Rating": float(row["IMDB rating"])
            })
            movie_id += 1
            for g in row["Genre"].split(" | "):
                genres.append({
                    "MovieId": movie_id,
                    "Genre": g
                })
                genre_id += 1
        return {"movies": movies, "genres": genres}

def save(filename, rows):
    keys = rows[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
