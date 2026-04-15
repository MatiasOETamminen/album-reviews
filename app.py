import secrets
import sqlite3
import markupsafe
import re
import math
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import db
import config
import users
import services

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    reviews = services.get_all_reviews()
    return render_template("index.html", reviews=reviews)

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
    return render_template("new_album.html", filled={})

@app.route("/create_album", methods=["POST"])
def create_album():
    require_login()
    check_csrf()
    artist = request.form["artist"].lower().strip()
    album = request.form["album"].lower().strip()
    year = request.form["year"]
    songlist = request.form["songlist"]
    genres_str = request.form["genres"].lower()
    filled = {"artist": artist, "album": album, "songlist": songlist,
              "genres": genres_str}
    if not artist or len(artist) > 1000:
        flash("The artist name can be at most 1,000 characters")
        return render_template("new_album.html", filled=filled)
    if not album or len(album) > 1000:
        flash("The album name can be at most 1,000 characters")
        return render_template("new_album.html", filled=filled)
    if not re.search("^[0-9]{4}$", year):
        flash("The year is not valid")
        return render_template("new_album.html", filled=filled)
    if not songlist or len(songlist) > 1500:
        flash("The songlist can be at most 1,500 characters")
        return render_template("new_album.html", filled=filled)
    if not genres_str or len(genres_str) > 1000:
        flash("The genre list can be at most 1,000 characters")
        return render_template("new_album.html", filled=filled)
    genres = [genre.strip() for genre in genres_str.split(";")]
    genre_ids = services.add_genres(genres)
    artist_id = services.add_artist(artist)
    try:
        services.add_album(artist_id, album, year, songlist, genre_ids)
    except sqlite3.IntegrityError:
        flash("This album already exists")
        return redirect("/" + str(artist) + "/" + str(album))
    return redirect("/" + str(artist) + "/" + str(album))

@app.route("/<artist>/<album>", methods=["GET", "POST"])
def show_album(artist, album, page=1):
    page_size = 10
    artist_id = services.get_artist(artist)
    review_count = services.count_album_reviews(artist_id, album)
    page_count = math.ceil(review_count / page_size)
    page_count = max(page_count, 1)
    review_average = services.albumaverage(artist_id, album)
    if not artist:
        abort(404)
    album_obj = services.get_album(artist_id, album)
    if not album_obj:
        abort(404)
    album = album_obj[0]
    year = album_obj[1]
    songlist = album_obj[2]
    genres = services.get_genres(artist_id, album)
    genres = [g[0] for g in genres]
    reviews = services.get_album_reviews(artist_id, album, page, page_size)
    album_data = {"artist": artist, "album": album,
                    "year": year, "songlist": songlist, "genres": genres}
    if request.method == "GET":
        return render_template("show_album.html", album_data=album_data,
                               reviews=reviews, review_count=review_count,
                               review_average=review_average, page=page,
                               page_count=page_count)
    if request.method == "POST":
        page = int(request.form["page"])
        if page < 1:
            page = 1
        if page > page_count:
            page = page_count
        reviews = services.get_album_reviews(artist_id, album, page, page_size)
        return render_template("show_album.html", album_data=album_data,
                               reviews=reviews, review_count=review_count,
                               review_average=review_average, page=page,
                               page_count=page_count)

@app.route("/albumsearch", methods=["GET", "POST"])
def albumsearch(page=1):
    page_size = 10
    if request.method == "GET":
        length = 0
        page_count = 1
        return render_template("search_album.html", results=None, filled={},
                               page=page, page_count=page_count)
    if request.method == "POST":
        album = request.form["album"].lower().strip()
        artist = request.form["artist"].lower().strip()
        genre = request.form["genre"].lower().strip()
        year = request.form["year"]
        page = int(request.form["page"])
        filled = {"artist": artist, "album": album, "genre": genre, "year": year}
        filled = {k: v if v else None for k, v in filled.items()}
        length = services.albumsearch_count(filled)
        album_obj = services.albumsearch(filled, page, page_size)
        page_count = math.ceil(length / page_size)
        page_count = max(page_count, 1)
        if page < 1:
            page = 1
        if page > page_count:
            page = page_count
        filled = {k: v if v is not None else "" for k, v in filled.items()}
        return render_template("search_album.html", album_obj=album_obj,
                               filled=filled, page=page, page_count=page_count)

@app.route("/<artist>/<album>/edit", methods=["GET", "POST"])
def edit_album(artist, album):
    require_login()
    artist_id = services.get_artist(artist)
    if not artist_id:
        abort(404)
    songlist = services.get_album(artist_id, album)[2]
    if not songlist:
        abort(404)
    if request.method == "GET":
        return render_template("edit_album.html", artist=artist, album=album,
                               songlist=songlist,genres=None)
    if request.method == "POST":
        check_csrf()
        content = request.form["songlist"]
        genres_str = request.form["genres"].lower()
        if len(genres_str) > 1000:
            flash("The genre list can be at most 1,000 characters")
            return render_template("edit_album.html", artist=artist, album=album,
                               songlist=songlist, genres=genres)
        genres = [genre.strip() for genre in genres_str.split(";")]
        genre_ids = services.add_genres(genres)
        services.update_genres(artist_id, album, genre_ids)
        services.update_album(artist_id, album, content)
        return redirect("/" + str(artist) + "/" + str(album))

@app.route("/<artist>/<album>/review", methods=["GET", "POST"])
def review_album(artist, album):
    require_login()
    user_id = session["user_id"]
    artist_id = services.get_artist(artist)
    if not artist_id:
        abort(404)
    album_obj = services.get_album(artist_id, album)
    if not album_obj:
        abort(404)
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
    return redirect("/" + str(artist) + "/" + str(album) + "/" + str(review_id))

@app.route("/<artist>/<album>/<int:review_id>")
def show_review(artist, album, review_id):
    artist_id = services.get_artist(artist)
    if not artist_id:
        abort(404)
    album_obj = services.get_album(artist_id, album)
    if not album_obj:
        abort(404)
    review = services.get_review(review_id)
    if not review:
        abort(404)
    albumreviews = services.get_review_ids(artist_id, album)
    found = False
    for albumreview in albumreviews:
        if int(albumreview[0]) == review_id:
            found = True
            break
    if not found:
        abort(404)
    username = services.get_username(review[0])
    comments = services.get_comments(review_id)
    return render_template("show_review.html", artist=artist, artist_id=artist_id,
                           album=album, review=review, review_id=review_id,
                           username=username, comments=comments)

@app.route("/<artist>/<album>/<int:review_id>/edit", methods=["GET", "POST"])
def edit_review(artist, album, review_id):
    require_login()
    artist_id = services.get_artist(artist)
    if not artist_id:
        abort(404)
    album_obj = services.get_album(artist_id, album)
    if not album_obj:
        abort(404)
    review = services.get_review(review_id)
    if not review:
        abort(404)
    albumreviews = services.get_review_ids(artist_id, album)
    found = False
    for albumreview in albumreviews:
        if int(albumreview[0]) == review_id:
            found = True
            break
    if not found:
        abort(404)
    if request.method == "GET":
        content = services.get_review(review_id)[1]
        filled = {"content": content}
        return render_template("edit_review.html", artist=artist, artist_id=artist_id,
                               album=album, review=review, review_id=review_id,
                               filled=filled)
    if request.method == "POST":
        check_csrf()
        content = request.form["content"]
        if not content:
            flash("The review cannot be empty")
            return render_template("new_review.html", artist=artist, album=album,
                                   review_id=review_id, filled={})
        if len(content) > 40000:
            flash("The length of the review can be at most 40,000 characters")
            filled = {"content": content}
            return render_template("new_review.html", artist=artist, album=album,
                                   review_id=review_id, filled=filled)
        grade = request.form["grade"]
        if not grade or grade not in {"1", "2", "3", "4", "5"}:
            flash("Please select a grade")
            filled = {"content": content}
            return render_template("new_review.html", artist=artist, album=album,
                                   review_id=review_id, filled=filled)
    services.edit_review(review_id, content, grade)
    return redirect("/" + str(artist + "/" + str(album) + "/" + str(review_id)))

@app.route("/<artist>/<album>/<int:review_id>/delete", methods=["GET", "POST"])
def delete_review(artist, album, review_id):
    require_login()
    artist_id = services.get_artist(artist)
    if not artist_id:
        abort(404)
    album_obj = services.get_album(artist_id, album)
    if not album_obj:
        abort(404)
    review = services.get_review(review_id)
    if not review:
        abort(404)
    albumreviews = services.get_review_ids(artist_id, album)
    found = False
    for albumreview in albumreviews:
        if int(albumreview[0]) == review_id:
            found = True
            break
    if not found:
        abort(404)
    if request.method == "GET":
        return render_template("delete_review.html", review=review, artist=artist,
                               album=album, review_id=review_id)
    if request.method == "POST":
        check_csrf()
        if "delete" in request.form:
            services.delete_review(review_id)
            return redirect("/" + str(artist) + "/" + str(album))
        return redirect("/" + str(artist) + "/" + str(album) + "/" + str(review_id))

@app.route("/comment", methods=["POST"])
def comment():
    require_login()
    check_csrf()
    content = request.form["content"]
    review_id = request.form["review_id"]
    user_id = session["user_id"]
    artist = request.form["artist"]
    album = request.form["album"]
    if not content or not review_id or not artist or not album:
        abort(403)
    services.add_comment(content, review_id, user_id)
    return redirect("/" + str(artist) + "/" + str(album) + "/" + str(review_id))

@app.route("/<int:user_id>")
def show_user(user_id):
    user_reviews = services.get_user_reviews(user_id)
    username = services.get_username(user_id)
    review_count = len(user_reviews)
    review_average = services.useraverage(user_id)
    return render_template("show_user.html", user_id=user_id, username=username,
                           user_reviews=user_reviews, review_count=review_count,
                           review_average=review_average)

@app.route("/usersearch", methods=["GET", "POST"])
def search_user():
    if request.method == "GET":
        return render_template("search_user.html", results=None, filled={})
    if request.method == "POST":
        username = request.form["name"].strip()
        filled = {"username": username}
        results = []
        if username:
            results += services.usersearch(username)
        return render_template("search_user.html", results=results, filled=filled)