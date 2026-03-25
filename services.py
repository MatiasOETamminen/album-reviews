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
    sql = """SELECT id from artists
             WHERE name = ?;"""
    return db.query(sql, [name])[0][0]

def get_artist_name(artist_id):
    sql = """SELECT name from artists
             WHERE id = ?;"""
    return db.query(sql, [artist_id])[0][0]

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
    sql = """SELECT id from genres
             WHERE name = ?;"""
    return db.query(sql, [genre])[0][0]

def get_genre_ids(artist_id, album):
    sql = """SELECT genre_id FROM albumgenres
             WHERE album_name = ? AND album_artist_id = ?;"""
    return db.query(sql, [album, artist_id])

def get_genre_name(genre_id):
    sql = """SELECT name FROM genres
             WHERE id = ?;"""
    return db.query(sql, [genre_id])[0][0]

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
    return db.query(sql, [artist_id, album])[0]
