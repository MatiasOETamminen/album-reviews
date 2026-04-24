import sqlite3

import db

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

def albumsearch(filled, page, page_size):
    sql = """SELECT lp.name, lp.artist_id, ar.name
             FROM albums AS lp
             LEFT JOIN artists AS ar
               ON lp.artist_id = ar.id
             LEFT JOIN albumgenres AS ag
               ON lp.name = ag.album_name AND lp.artist_id = ag.album_artist_id
             LEFT JOIN genres AS g
               ON g.id = ag.genre_id
             WHERE lp.name LIKE COALESCE(?, lp.name)
               AND ar.name LIKE COALESCE(?, ar.name)
               AND g.name = COALESCE(?, g.name)
               AND lp.year = COALESCE(?, lp.year)
             GROUP BY lp.name, lp.artist_id
             LIMIT ? OFFSET ?;"""

    limit = page_size
    offset = page_size * (page - 1)
    arguments = [
        "%" + filled["album"] + "%" if filled["album"] else None,
        "%" + filled["artist"] + "%" if filled["artist"] else None,
        filled["genre"],
        filled["year"],
        limit,
        offset
    ]

    return db.query(sql, arguments)

def albumsearch_count(filled):
    sql = """SELECT COUNT(DISTINCT lp.name || '|' || ar.name)
             FROM albums AS lp
             LEFT JOIN artists AS ar
               ON lp.artist_id = ar.id
             LEFT JOIN albumgenres AS ag
               ON lp.name = ag.album_name AND lp.artist_id = ag.album_artist_id
             LEFT JOIN genres AS g
               ON g.id = ag.genre_id
             WHERE lp.name LIKE COALESCE(?, lp.name)
               AND ar.name LIKE COALESCE(?, ar.name)
               AND g.name = COALESCE(?, g.name)
               AND lp.year = COALESCE(?, lp.year);"""

    arguments = [
        "%" + filled["album"] + "%" if filled["album"] else None,
        "%" + filled["artist"] + "%" if filled["artist"] else None,
        filled["genre"],
        filled["year"],
    ]

    return db.query(sql, arguments)[0][0]

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

def get_genres(artist_id, album):
    sql = """SELECT g.name
             FROM genres AS g, albumgenres AS ag
             WHERE g.id = ag.genre_id
             AND ag.album_name = ?
             AND ag.album_artist_id = ?;"""
    return db.query(sql, [album, artist_id])

def add_album(artist_id, album, year, songlist, genre_ids):
    sql = """INSERT INTO albums (artist_id, name, year, songlist)
             VALUES (?, ?, ?, ?);"""
    db.execute(sql, [artist_id, album, year, songlist])
    for genre in genre_ids:
        sql = """INSERT INTO albumgenres (album_name, album_artist_id, genre_id)
                 VALUES (?, ?, ?);"""
        db.execute(sql, [album, artist_id, genre])

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
        except sqlite3.IntegrityError:
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

def get_review(review_id, artist_id, album):
    sql = """SELECT user_id, content, grade, sent_at, edited_at FROM reviews
             WHERE id = ? AND album_artist_id = ? AND album_name = ?;"""
    result = db.query(sql, [review_id, artist_id, album])
    return result[0] if result else None

def get_review_ids(artist_id, album):
    sql = """SELECT id FROM reviews
             WHERE album_artist_id = ?
             AND album_name = ?;"""
    return db.query(sql, [artist_id, album])

def count_album_reviews(artist_id, album):
    sql = """SELECT COUNT(id)
             FROM reviews
             WHERE album_name = ?
             AND album_artist_id = ?;"""
    return db.query(sql, [album, artist_id])[0][0]

def get_album_reviews(artist_id, album, page, page_size):
    sql = """SELECT r.id, u.id, u.username, lp.name, ar.name,
             r.grade, r.sent_at, r.edited_at
             FROM reviews AS r
             LEFT JOIN users AS u
               ON r.user_id = u.id
             LEFT JOIN artists AS ar
               ON r.album_artist_id = ar.id
             LEFT JOIN albums AS lp
               ON lp.name = r.album_name AND lp.artist_id = ar.id
             WHERE ar.id = ? AND lp.name = ?
             GROUP BY r.id
             ORDER BY r.sent_at DESC
             LIMIT ? OFFSET ?;
             """
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [artist_id, album, limit, offset])

def delete_review(review_id):
    sql = """DELETE FROM comments WHERE review_id = ?;"""
    db.execute(sql, [review_id])
    sql = """DELETE FROM reviews WHERE id = ?;"""
    db.execute(sql, [review_id])

def count_all_reviews():
    sql = """SELECT COUNT(id) FROM reviews;"""
    return db.query(sql)[0][0]

def get_all_reviews(page, page_size):
    sql = """SELECT r.id, u.username, r.album_name, a.name, r.grade, r.sent_at,
             r.edited_at, u.id
             FROM reviews AS r, users AS u, artists AS a
             WHERE r.user_id = u.id AND r.album_artist_id = a.id
             ORDER BY r.sent_at DESC
             LIMIT ? OFFSET ?;"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_username(user_id):
    sql = """SELECT username FROM users
             WHERE id = ?;"""
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def count_user_reviews(user_id):
    sql = """SELECT COUNT(id), ROUND(AVG(grade), 2) FROM reviews
             WHERE user_id = ?;"""
    return db.query(sql, [user_id])[0]

def get_user_reviews(user_id, page, page_size):
    sql = """SELECT r.id, u.username, r.album_name, a.name, r.grade, r.sent_at,
             r.edited_at
             FROM reviews AS r, users AS u, artists AS a
             WHERE u.id = ?
             AND r.user_id = u.id
             AND r.album_artist_id = a.id
             ORDER BY r.sent_at DESC
             LIMIT ? OFFSET ?;"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [user_id, limit, offset])

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

def count_comments(review_id):
    sql = """SELECT COUNT(id) FROM comments
             WHERE review_id = ?;"""
    return db.query(sql, [review_id])[0][0]

def get_comments(review_id, page, page_size):
    sql = """SELECT c.id, c.review_id, c.user_id, u.username, c.content,
             c.sent_at, c.edited_at
             FROM comments AS c, users AS u
             WHERE c.user_id = u.id AND c.review_id = ?
             ORDER BY c.sent_at DESC
             LIMIT ? OFFSET ?;"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [review_id, limit, offset])

def usersearch_count(name):
    sql = """SELECT COUNT(id) FROM users
             WHERE username LIKE ?
             COLLATE NOCASE;"""
    return db.query(sql, ["%" + name + "%"])[0][0]

def usersearch(name, page, page_size):
    sql = """SELECT id, username FROM users
             WHERE username LIKE ?
             COLLATE NOCASE
             LIMIT ? OFFSET ?;"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, ["%" + name + "%", limit, offset])
