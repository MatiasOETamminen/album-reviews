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

def get_artist_fuzzy(name):
    sql = """SELECT id FROM artists
             WHERE name LIKE ?;"""
    return db.query(sql, ["%" + name + "%"])

def artistsearch(artist_ids):
    if not artist_ids:
        return []
    placeholders = ",".join(["?"] * len(artist_ids))
    sql = f"""
        SELECT name, artist_id
        FROM albums
        WHERE artist_id IN ({placeholders});"""
    return db.query(sql, artist_ids)

def genresearch(id):
    sql = """SELECT a.name, a.artist_id
             FROM albums AS a, albumgenres AS g
             WHERE g.genre_id = ? AND
             g.album_name = a.name AND
             g.album_artist_id = a.artist_id;"""
    return db.query(sql, [id])

def yearsearch(year):
    sql = """SELECT name, artist_id FROM albums
             WHERE year = ?;"""
    return db.query(sql, [year])

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

def update_genres(artist_id, album, genre_ids):
    for genre_id in genre_ids:
        try:
            sql = """INSERT INTO albumgenres (album_name, album_artist_id, genre_id)
                    VALUES (?, ?, ?);"""
            db.execute(sql, [album, artist_id, genre_id])
        except:
            pass

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

def delete_review(review_id):
    sql = """DELETE FROM comments WHERE review_id = ?;"""
    db.execute(sql, [review_id])
    sql = """DELETE FROM reviews WHERE id = ?;"""
    db.execute(sql, [review_id])

def get_all_reviews():
    sql = """SELECT r.id, u.username, r.album_name, a.name, r.grade, r.sent_at,
             r.edited_at, u.id
             FROM reviews AS r, users AS u, artists AS a
             WHERE r.user_id = u.id AND r.album_artist_id = a.id
             ORDER BY r.sent_at DESC;"""
    return db.query(sql)

def get_username(user_id):
    sql = """SELECT username FROM users
             WHERE id = ?;"""
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def get_user_reviews(user_id):
    sql = """SELECT r.id, u.username, r.album_name, a.name, r.grade, r.sent_at,
             r.edited_at
             FROM reviews AS r, users AS u, artists AS a
             WHERE u.id = ?
             AND r.user_id = u.id
             AND r.album_artist_id = a.id
             ORDER BY r.sent_at DESC;"""
    return db.query(sql, [user_id])

def useraverage(user_id):
    sql = """SELECT ROUND(AVG(grade), 2) FROM reviews WHERE user_id = ?;"""
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def albumaverage(artist_id, name):
    sql = """SELECT ROUND(AVG(grade), 2) FROM reviews
             WHERE album_artist_id = ?
             AND album_name = ?;"""
    result = db.query(sql, [artist_id, name])
    return result[0][0] if result else None

def add_comment(content, review_id, user_id):
    sql = """INSERT INTO comments (review_id, user_id, content, sent_at)
             VALUES (?, ?, ?, datetime('now'));"""
    db.execute(sql, [review_id, user_id, content])

def get_comments(review_id):
    sql = """SELECT c.id, c.review_id, c.user_id, u.username, c.content, 
             c.sent_at, c.edited_at
             FROM comments AS c, users AS u
             WHERE c.user_id = u.id AND c.review_id = ?;"""
    return db.query(sql, [review_id])

def usersearch(name):
    sql = """SELECT id, username FROM users
             WHERE username LIKE ?
             COLLATE NOCASE;"""
    return db.query(sql, ["%" + name + "%"])