

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
    movies.genre,
    ratings.rating
FROM ratings
INNER JOIN movies ON ratings.movieID = movies.id
WHERE movieID = 1
ORDER BY ratings.movieID ASC;

-- @block
SELECT movies.title, movies.genre, ratings.rating FROM ratings INNER JOIN movies ON ratings.movieID = movies.id WHERE movieID = 4;

-- @block
SELECT
    movies.title, 
    movies.genre, 
    GROUP_CONCAT(ratings.rating ORDER BY ratings.rating ASC) AS all_ratings 
FROM movies 
INNER JOIN ratings ON ratings.movieID = movies.id 
WHERE ratings.movieID = 2 
GROUP BY movies.id, movies.title, movies.genre;


-- @block
INSERT INTO ratings (movieID, rating, userID)
VALUES
    (1, 5, 3),
    (1, 3, 4),
    (1, 1, 5),
    (1, 5, 6);

-- @block
SELECT * FROM ratings
WHERE movieID = 1