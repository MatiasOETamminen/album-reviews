# Album Reviews

## Application functionality

* A user can create a user account and log into the application.
* A user can add albums to the database.
* A user can edit the songlist and add genres to albums in the database.
* A user can add reviews for albums in the database.
* A user can modify or remove their own reviews
* A user can see all reviews on the platform.
* Every album has an album page that shows the album metadata and all the reviews for that album.
* A user can search albums based on album name, album artist, year, or genre.
* Every user has a user page that shows all the reviews the user has published as well as some simple stats.
* A user can search users based on username.
* Users can comment on reviews.

## Installation

Install the `flask` library:

```
$ pip install flask
```

Initialize the database:

```
$ sqlite3 database.db < schema.sql
```

You can launch the application with:

```
$ flask run
```