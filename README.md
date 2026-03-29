# Album Reviews

## Application functionality

* A user can create a user account and log into the application.
* A user can add albums to the database.
* A user can edit the songlist and add genres to albums in the database.
* A user can add, modify, and remove reviews for albums in the database.
* A user can see all reviews on the platform.
* A user can search reviews based on album name, album artist, year, genre, or the user that has written the review.
* Every user has a user page that shows all the reviews the user has published.
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