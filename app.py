import secrets
import sqlite3
import markupsafe
import re
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import users
import services

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("ERROR: the passwords don't match")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("ERROR: The selected username is already in use")
        return redirect("/register")

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        flash("ERROR: Either the username or the password is incorrect")
        return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/new_album")
def new_album():
    require_login()
    return render_template("new_album.html")

@app.route("/create_album", methods=["POST"])
def create_album():
    require_login()
    check_csrf()
    artist = request.form["artist"].lower().strip()
    if not artist or len(artist) > 1000:
        abort(403)
    album = request.form["album"].lower().strip()
    if not album or len(album) > 1000:
        abort(403)
    year = request.form["year"]
    if not re.search("^[0-9]{4}$", year):
        abort(403)
    songlist = request.form["songlist"]
    if not songlist or len(songlist) > 1500:
        abort(403)
    genres_str = request.form["genres"].lower()
    if not genres_str or len(genres_str) > 1000:
        abort(403)
    genres = [genre.strip() for genre in genres_str.split(";")]
    genre_ids = services.add_genres(genres)
    artist_id = services.add_artist(artist)
    services.add_album(artist_id, album, year, songlist, genre_ids)
    return redirect("/" + str(artist) + "/" + str(album))

@app.route("/<artist>/<album>")
def show_album(artist, album):
    artist_id = services.get_artist(artist)
    if not artist:
        abort(404)
    artist = services.get_artist_name(artist_id)
    album_obj = services.get_album(artist_id, album)
    album = album_obj[0]
    year = album_obj[1]
    songlist = album_obj[2]
    genre_ids = [g[0] for g in services.get_genre_ids(artist_id, album)]
    genres = []
    for genre_id in genre_ids:
        genres.append(services.get_genre_name(genre_id))
    review_ids = services.get_review_ids(artist_id, album)
    reviews = []
    for review_id in review_ids:
        review_obj = services.get_review(review_id[0])
        username = services.get_username(review_obj[0])
        reviews.append((review_obj, username, review_id[0]))
    return render_template("show_album.html", artist=artist, album=album,
                           year=year, songlist=songlist, genres=genres,
                           reviews=reviews)

@app.route("/search_album")
def search_album():
    return render_template("search_album.html")

@app.route("/albumsearch", methods=["POST"])
def albumsearch():
    album = request.form["album"].lower().strip()
    album_obj = services.albumsearch(album)
    results = []
    for obj in album_obj:
        artist_name = services.get_artist_name(obj[1])
        results.append((obj[0], artist_name))
    return render_template("search_album.html", results=results)

@app.route("/<artist>/<album>/edit", methods=["GET", "POST"])
def edit_album(artist, album):
    require_login()
    artist_id = services.get_artist(artist)
    songlist = services.get_album(artist_id, album)[2]
    if request.method == "GET":
        return render_template("edit_album.html", artist=artist, album=album,
                               songlist=songlist)
    if request.method == "POST":
        check_csrf()
        content = request.form["songlist"]
        services.update_album(artist_id, album, content)
        return redirect("/" + str(artist) + "/" + str(album))

@app.route("/<artist>/<album>/review", methods=["GET", "POST"])
def review_album(artist, album):
    require_login()
    user_id = session["user_id"]
    artist_id = services.get_artist(artist)
    if request.method == "GET":
        return render_template("new_review.html", artist=artist, album=album,
                               filled={})
    if request.method == "POST":
        check_csrf()
        content = request.form["content"]
        if not content:
            flash("The review cannot be empty")
            return render_template("new_review.html", artist=artist, album=album,
                                   filled={})
        if len(content) > 40000:
            flash("The length of the review can be at most 40,000 characters")
            filled = {"content": content}
            return render_template("new_review.html", artist=artist, album=album,
                                   filled=filled)
        grade = request.form["grade"]
        if not grade or grade not in {"1", "2", "3", "4", "5"}:
            flash("Please select a grade")
            filled = {"content": content}
            return render_template("new_review.html", artist=artist, album=album,
                                   filled=filled)
    services.add_review(user_id, album, artist_id, content, grade)
    review_id = db.last_insert_id()
    return redirect("/" + str(artist + "/" + str(album) + "/" + str(review_id)))

@app.route("/<artist>/<album>/<int:review_id>")
def show_review(artist, album, review_id):
    artist_id = services.get_artist(artist)
    review = services.get_review(review_id)
    return render_template("show_review.html", artist=artist, artist_id=artist_id,
                           album=album, review=review)

def require_login():
    if "user_id" not in session:
        abort(403)