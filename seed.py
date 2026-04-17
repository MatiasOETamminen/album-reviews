import sqlite3
from werkzeug.security import generate_password_hash

db = sqlite3.connect("database.db")

db.execute("DELETE FROM artists")
db.execute("DELETE FROM albums")
db.execute("DELETE FROM users")
db.execute("DELETE FROM reviews")
db.execute("DELETE FROM genres")
db.execute("DELETE FROM albumgenres")
db.execute("DELETE FROM comments")

db.execute("PRAGMA foreign_keys = ON")

user_count = 1000
artist_count = 10**3
album_count = 10**5
review_count = 10**7
comment_count = 10**9
sample_genres = {1: "country", 2: "electronic", 3: "funk", 4: "hip-hop",
                 5: "jazz", 6: "latin", 7: "pop", 8: "rock", 9: "blues",
                 10: "r&b"}

for i in range(1, user_count + 1):
    password = generate_password_hash("1")
    username = "Sample" + str(i)
    sql = """INSERT INTO users (username, password_hash) VALUES (?, ?);"""
    db.execute(sql, [username, password])

for i in range(1, artist_count + 1):
    name = "Sample artist" + str(i)
    sql = """INSERT INTO artists (name) VALUES (?);"""
    db.execute(sql, [name])

for k, v in sample_genres.items():
    sql = """INSERT INTO genres (name) VALUES (?);"""
    db.execute(sql, [v])

for i in range(1, album_count + 1):
    name = "Sample album" + str(i)
    artist_id = i % artist_count + 1
    year = 1901 + i % 100
    songlist = """1. Lorem
                  2. Ipsum
                  3. Dolor
                  4. Sit
                  5. Amet
                  6. Consectetur
                  7. Adipiscing
                  8. Elit
                  9. Sed
                  10. Do"""
    sql = """INSERT INTO albums (name, artist_id, year, songlist)
             VALUES (?, ?, ?, ?);"""
    db.execute(sql, [name, artist_id, year, songlist])
    sql = """INSERT INTO albumgenres (album_name, album_artist_id, genre_id)
             VALUES (?, ?, ?);"""
    db.execute(sql, [name, artist_id, i % 10 + 1])

for i in range(1, review_count + 1):
    user_id = i % user_count + 1
    album_name = "Sample album" + str(i % album_count + 1)
    album_artist_id = (i % album_count + 1) % artist_count + 1
    content = "Lorem ipsum dolor sit amet"
    grade = (i % 1337 + 1) % 5 + 1
    sql = """INSERT INTO reviews (user_id, album_name, album_artist_id,
             content, grade, sent_at)
             VALUES (?, ?, ?, ?, ?, datetime('now'));"""
    db.execute(sql, [user_id, album_name, album_artist_id, content, grade])

for i in range(1, comment_count + 1):
    review_id = i % review_count + 1
    user_id = i % user_count + 1
    content = "Sample comment" + str(i)
    sql = """INSERT INTO comments (review_id, user_id, content, sent_at)
             VALUES (?, ?, ?, datetime('now'));"""
    db.execute(sql, [review_id, user_id, content])

db.commit()
db.close()