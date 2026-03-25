CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    album_id INTEGER REFERENCES albums,
    content TEXT,
    grade INTEGER
);

CREATE TABLE albums (
    id INTEGER PRIMARY KEY,
    name TEXT,
    artist REFERENCES artists,
    year INTEGER,
    cover BLOB,
    songlist TEXT
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE albumgenres (
    album_id INTEGER REFERENCES albums,
    genre_id INTEGER REFERENCES genres,
    PRIMARY KEY (album_id, genre_id)
);

CREATE TABLE artists (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews,
    user_id INTEGER REFERENCES users,
    content TEXT
);