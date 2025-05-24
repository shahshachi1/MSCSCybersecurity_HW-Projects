-- Shachi Shah
-- SQL Query for Movie Recommendation Assignment

DROP TABLE IF EXISTS query1;
DROP TABLE IF EXISTS query2;
DROP TABLE IF EXISTS query3;
DROP TABLE IF EXISTS query4;
DROP TABLE IF EXISTS query5;
DROP TABLE IF EXISTS query6;
DROP TABLE IF EXISTS query7;
DROP TABLE IF EXISTS query8;
DROP TABLE IF EXISTS query9;

-- Query 1: Total number of movies for each genre
CREATE TABLE query1 AS
SELECT g.name, COUNT(mg.movieid) AS moviecount
FROM genres g
JOIN hasagenre mg ON g.genreid = mg.genreid
GROUP BY g.name;

-- Query 2: Average rating per genre
CREATE TABLE query2 AS
SELECT g.name, AVG(r.rating) AS rating
FROM genres g
JOIN hasagenre mg ON g.genreid = mg.genreid
JOIN ratings r ON mg.movieid = r.movieid
GROUP BY g.name;

-- Query 3: Movies with at least 10 ratings
CREATE TABLE query3 AS
SELECT m.title, COUNT(r.rating) AS countofratings
FROM movies m
JOIN ratings r ON m.movieid = r.movieid
GROUP BY m.title
HAVING COUNT(r.rating) >= 10;

-- Query 4: All movies that belong to the "Comedy" genre
CREATE TABLE query4 AS
SELECT m.movieid, m.title
FROM movies m
JOIN hasagenre mg ON m.movieid = mg.movieid
JOIN genres g ON mg.genreid = g.genreid
WHERE g.name = 'Comedy';

-- Query 5: Average rating per movie
CREATE TABLE query5 AS
SELECT m.title, AVG(r.rating) AS average
FROM movies m
JOIN ratings r ON m.movieid = r.movieid
GROUP BY m.title;

-- Query 6: Average rating of all movies that are in the "Comedy" genre
CREATE TABLE query6 AS
SELECT AVG(r.rating) AS average
FROM ratings r
JOIN hasagenre mg ON r.movieid = mg.movieid
JOIN genres g ON mg.genreid = g.genreid
WHERE g.name = 'Comedy';

-- Query 7: Average rating of movies that are both "Comedy" AND "Romance"
CREATE TABLE query7 AS
SELECT AVG(r.rating) AS average
FROM ratings r
WHERE r.movieid IN (
  SELECT mg1.movieid
  FROM hasagenre mg1
  JOIN genres g1 ON mg1.genreid = g1.genreid
  WHERE g1.name = 'Comedy'
  INTERSECT
  SELECT mg2.movieid
  FROM hasagenre mg2
  JOIN genres g2 ON mg2.genreid = g2.genreid
  WHERE g2.name = 'Romance'
);

-- Query 8: Average rating of movies that are "Romance" but NOT "Comedy"
CREATE TABLE query8 AS
SELECT AVG(r.rating) AS average
FROM ratings r
WHERE r.movieid IN (
  SELECT mg1.movieid
  FROM hasagenre mg1
  JOIN genres g1 ON mg1.genreid = g1.genreid
  WHERE g1.name = 'Romance'
  EXCEPT
  SELECT mg2.movieid
  FROM hasagenre mg2
  JOIN genres g2 ON mg2.genreid = g2.genreid
  WHERE g2.name = 'Comedy'
);

-- Query 9: Movies rated by a user with ID equal to :v1 (parameter passed at runtime)
CREATE TABLE query9 AS
SELECT movieid, rating
FROM ratings
WHERE userid = :v1;
