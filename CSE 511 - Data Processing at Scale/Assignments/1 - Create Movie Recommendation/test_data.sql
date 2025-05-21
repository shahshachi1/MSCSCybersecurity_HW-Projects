-- Insert users
INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');

-- Insert movies
INSERT INTO movies VALUES (100, 'The Matrix'), (200, 'Inception');

-- Insert genres
INSERT INTO genres VALUES (1, 'Sci-Fi'), (2, 'Action');

-- Insert taginfo
INSERT INTO taginfo VALUES (1, 'cool'), (2, 'mind-bending');

-- Insert valid ratings
INSERT INTO ratings VALUES (1, 100, 5, 1685000000);
INSERT INTO ratings VALUES (2, 200, 4.5, 1685000100);

-- Insert tags
INSERT INTO tags VALUES (1, 100, 1, 1685000200);
INSERT INTO tags VALUES (2, 200, 2, 1685000300);

-- Insert hasagenre
INSERT INTO hasagenre VALUES (100, 1), (100, 2), (200, 1);

-- Rating out of range
INSERT INTO ratings VALUES (1, 100, 6, 1685000001);

-- Duplicate rating
INSERT INTO ratings VALUES (1, 100, 4, 1685000002);

-- Invalid foreign key (nonexistent genre)
INSERT INTO hasagenre VALUES (200, 999);

-- Invalid tagid
INSERT INTO tags VALUES (1, 100, 999, 1685000301);

