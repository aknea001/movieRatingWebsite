-- @block
CREATE TABLE users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(2)
);

-- @block
CREATE TABLE movies(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(50)
);

-- @block
CREATE TABLE ratings(
    id INT AUTO_INCREMENT,
    userID INT NOT NULL,
    movieID INT NOT NULL,
    rating INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (userID) REFERENCES users(id),
    FOREIGN KEY (movieID) REFERENCES movies(id)
);

-- @block
INSERT INTO movies (title, genre)
VALUES
    ("Fight club", "Action thriller"),
    ("The silence of the lambs", "Horror thriller"),
    ("Shrek", "Family comedy");

-- @block
SELECT * FROM ratings;

-- @block
