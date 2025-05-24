-- Shachi Shah
-- Create Movie Recommendation Database Assignment

-- USERS TABLE
CREATE TABLE users (
    userid INTEGER PRIMARY KEY,
    name TEXT
);

-- MOVIES TABLE
CREATE TABLE movies (
    movieid INTEGER PRIMARY KEY,
    title TEXT
);

-- TAGINFO TABLE
CREATE TABLE taginfo (
    tagid INTEGER PRIMARY KEY,
    content TEXT
);

-- GENRES TABLE
CREATE TABLE genres (
    genreid INTEGER PRIMARY KEY,
    name TEXT
);

-- RATINGS TABLE
CREATE TABLE ratings (
    userid INTEGER,
    movieid INTEGER,
    rating NUMERIC CHECK (rating >= 0 AND rating <= 5),
    timestamp BIGINT,
    PRIMARY KEY (userid, movieid),
    FOREIGN KEY (userid) REFERENCES users(userid),
    FOREIGN KEY (movieid) REFERENCES movies(movieid)
);

-- TAGS TABLE
CREATE TABLE tags (
    userid INTEGER,
    movieid INTEGER,
    tagid INTEGER,
    timestamp BIGINT,
    FOREIGN KEY (userid) REFERENCES users(userid),
    FOREIGN KEY (movieid) REFERENCES movies(movieid),
    FOREIGN KEY (tagid) REFERENCES taginfo(tagid)
);

-- HASAGENRE TABLE
CREATE TABLE hasagenre (
    movieid INTEGER,
    genreid INTEGER,
    PRIMARY KEY (movieid, genreid),
    FOREIGN KEY (movieid) REFERENCES movies(movieid),
    FOREIGN KEY (genreid) REFERENCES genres(genreid)
);

