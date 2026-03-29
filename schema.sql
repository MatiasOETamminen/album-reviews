CREATE TABLE artists (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE albums (
    name TEXT,
    artist_id INTEGER NOT NULL,
    year INTEGER,
    cover BLOB,
    songlist TEXT,
    PRIMARY KEY (name, artist_id),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    album_name TEXT NOT NULL,
    album_artist_id INTEGER NOT NULL,
    content TEXT,
    grade INTEGER,
    sent_at TEXT,
    edited_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (album_name, album_artist_id)
        REFERENCES albums(name, artist_id)
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE albumgenres (
    album_name TEXT NOT NULL,
    album_artist_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (album_name, album_artist_id, genre_id),
    FOREIGN KEY (album_name, album_artist_id)
        REFERENCES albums(name, artist_id),
    FOREIGN KEY (genre_id)
        REFERENCES genres(id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    review_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT,
    sent_at TEXT,
    edited_at TEXT,
    FOREIGN KEY (review_id) REFERENCES reviews(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
