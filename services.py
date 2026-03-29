import db
import sqlite3

def add_artist(name):
    try:
        sql = """INSERT INTO artists (name)
                 VALUES (?);"""
        db.execute(sql, [name])
    except sqlite3.IntegrityError:
        pass
    name = get_artist(name)
    return name

def get_artist(name):
    sql = """SELECT id FROM artists
             WHERE name = ?;"""
    result = db.query(sql, [name])
    return result[0][0] if result else None

def albumsearch(name):
    sql = """SELECT name, artist_id FROM albums
             WHERE name LIKE ?;"""
    return db.query(sql, ["%" + name + "%"])

def get_artist_name(artist_id):
    sql = """SELECT name FROM artists
             WHERE id = ?;"""
    result = db.query(sql, [artist_id])
    return result[0][0] if result else None

def add_genres(genres):
    genre_ids = []
    for genre in genres:
        try:
            sql = """INSERT INTO genres (name)
                    VALUES (?);"""
            db.execute(sql, [genre])
        except sqlite3.IntegrityError:
            pass
        genre_ids.append(get_genre(genre))
    return genre_ids

def get_genre(genre):
    sql = """SELECT id FROM genres
             WHERE name = ?;"""
    result = db.query(sql, [genre])
    return result[0][0] if result else None

def get_genre_ids(artist_id, album):
    sql = """SELECT genre_id FROM albumgenres
             WHERE album_name = ? AND album_artist_id = ?;"""
    return db.query(sql, [album, artist_id])

def get_genre_name(genre_id):
    sql = """SELECT name FROM genres
             WHERE id = ?;"""
    result = db.query(sql, [genre_id])
    return result[0][0] if result else None

def add_album(artist_id, album, year, songlist, genre_ids):
    sql = """INSERT INTO albums (artist_id, name, year, songlist)
             VALUES (?, ?, ?, ?);"""
    db.execute(sql, [artist_id, album, year, songlist])
    for genre in genre_ids:
        sql = """INSERT INTO albumgenres (album_name, album_artist_id, genre_id)
                 VALUES (?, ?, ?);"""
        db.execute(sql, [album, artist_id, genre])
    return [album, artist_id, genre]

def get_album(artist_id, album):
    sql = """SELECT name, year, songlist FROM albums
             WHERE artist_id = ? AND name = ?;"""
    result = db.query(sql, [artist_id, album])
    return result[0] if result else None

def update_album(artist_id, album, songlist):
    sql = """UPDATE albums SET songlist = ?
             WHERE artist_id = ? AND name = ?;"""
    db.execute(sql, [songlist, artist_id, album])

def add_review(user_id, album, artist_id, content, grade):
    sql = """INSERT INTO reviews (user_id, album_name, album_artist_id, content,
             grade, sent_at)
             VALUES (?, ?, ?, ?, ?, datetime('now'));"""
    db.execute(sql, [user_id, album, artist_id, content, grade])

def edit_review(review_id, content, grade):
    sql = """UPDATE reviews SET content = ?, grade = ?, edited_at = datetime('now')
             WHERE id = ?;"""
    db.execute(sql, [content, grade, review_id])

def get_review(review_id):
    sql = """SELECT user_id, content, grade, sent_at, edited_at FROM reviews
             WHERE id = ?;"""
    result = db.query(sql, [review_id])
    return result[0] if result else None

def get_review_ids(artist_id, album):
    sql = """SELECT id FROM reviews
             WHERE album_artist_id = ?
             AND album_name = ?;"""
    return db.query(sql, [artist_id, album])

def get_username(user_id):
    sql = """SELECT username FROM users
             WHERE id = ?;"""
    result = db.query(sql, [user_id])
    return result[0][0] if result else None