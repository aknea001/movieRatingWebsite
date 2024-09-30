

-- @block
SELECT * FROM users;

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
WHERE ratings.movieID = 4 
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

-- @block
SELECT
    IF(rating IS NULL AND movieID = 1,
        (SELECT title, genre FROM movies WHERE id = 1),
        (SELECT movies.title, movies.genre, GROUP_CONCAT(ratings.rating ORDER BY ratings.rating ASC) AS all_ratings FROM movies INNER JOIN ratings ON ratings.movieID = movies.id WHERE ratings.movieID = 2 GROUP BY movies.id, movies.title, movies.genre)
    ) AS result
    FROM ratings;

-- @block
SELECT
    movies.title,
    movies.genre,
    CASE 
        WHEN ratings.rating IS NULL AND ratings.movieID = 1 THEN
            'Movie has no ratings (NULL)'
        ELSE 
            GROUP_CONCAT(ratings.rating ORDER BY ratings.rating ASC)
    END AS all_ratings
FROM 
    movies
LEFT JOIN 
    ratings ON ratings.movieID = movies.id
WHERE 
    movies.id IN (1, 2)
GROUP BY 
    movies.id, movies.title, movies.genre;


-- @block
SELECT movies.title, movies.genre, GROUP_CONCAT(ratings.rating ORDER BY ratings.rating ASC) AS all_ratings FROM movies INNER JOIN ratings ON ratings.movieID = movies.id WHERE ratings.movieID = 4 GROUP BY movies.id, movies.title, movies.genre