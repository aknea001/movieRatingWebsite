

-- @block
SELECT * FROM movies;

-- @block
INSERT INTO movies (title, genre)
VALUES
    ("Shrek 2", "Family Comedy"),
    ("Shrek the Third", "Family Comedy"),
    ("Shrek forever after", "Family Comedy"),
    ("Shrek 3D", "Family Comedy");

-- @block
SELECT
    movies.title,
    ratings.rating,
    users.email
FROM ratings
INNER JOIN movies on ratings.movieID = movies.id
INNER JOIN users on ratings.userID = users.id
ORDER BY movieID ASC;