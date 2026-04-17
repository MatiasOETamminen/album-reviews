# Testing the application with large data volumes

## Preparing the test data and methods
I used [seed.py](./seed.py) to initialize the database with 1,000 users, 1,000 artists, 100,000 albums, 10,000,000 reviews, and 1,000,000,000 comments.

I also added the following functions to to [app.py](./app.py):
```py
@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response
```

## Index page
Opening the index page and paging through the latest reviews felt quite unresponsive. Looking at the printouts, the elapsed time was over a second for each page load:

```
elapsed time: 1.4 s
127.0.0.1 - - [17/Apr/2026 12:31:44] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:31:44] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 1.38 s
127.0.0.1 - - [17/Apr/2026 12:32:25] "POST / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:32:25] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 1.37 s
127.0.0.1 - - [17/Apr/2026 12:32:32] "POST / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:32:32] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 1.41 s
127.0.0.1 - - [17/Apr/2026 12:32:35] "POST / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:32:35] "GET /static/main.css HTTP/1.1" 304 -
```

I made this faster by creating these two indices, verifying one by one that they help:

```sql
CREATE INDEX idx_user_id ON reviews(user_id);
CREATE INDEX idx_sent_at ON reviews(sent_at DESC);
```

After that change, the index page loaded and changed pages in less than 0.3 seconds:

```
elapsed time: 0.26 s
127.0.0.1 - - [17/Apr/2026 14:08:55] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:08:55] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.27 s
127.0.0.1 - - [17/Apr/2026 14:08:58] "POST / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:08:58] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.27 s
127.0.0.1 - - [17/Apr/2026 14:08:59] "POST / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:08:59] "GET /static/main.css HTTP/1.1" 304 -

```

## Album page
Looking at an album and paging through the reviews there was similar to the index page before the added indices:

```
elapsed time: 1.28 s
127.0.0.1 - - [17/Apr/2026 12:36:15] "GET /Sample%20artist941/Sample%20album97940 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:36:15] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 1.27 s
127.0.0.1 - - [17/Apr/2026 12:36:21] "POST /Sample%20artist941/Sample%20album97940 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:36:21] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 1.27 s
127.0.0.1 - - [17/Apr/2026 12:36:27] "POST /Sample%20artist941/Sample%20album97940 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:36:27] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 1.29 s
127.0.0.1 - - [17/Apr/2026 12:36:30] "POST /Sample%20artist941/Sample%20album97940 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:36:30] "GET /static/main.css HTTP/1.1" 304 -
```

To make that faster, I added the following index:

```sql
CREATE INDEX idx_albumreviews ON reviews(album_artist_id, album_name, sent_at DESC);
```

After the index was added, the page loaded and changed pages instantaneously:

```
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:16:35] "GET /Sample%20artist931/Sample%20album97930 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:16:35] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:16:40] "POST /Sample%20artist931/Sample%20album97930 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:16:40] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:16:42] "POST /Sample%20artist931/Sample%20album97930 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:16:42] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:16:44] "POST /Sample%20artist931/Sample%20album97930 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:16:44] "GET /static/main.css HTTP/1.1" 304 -
```

## User page
Looking at a user page and paging through the user's reviews was already really quick after the aforementioned indexing additions. No additional indices were needed here:

```
elapsed time: 0.03 s
127.0.0.1 - - [17/Apr/2026 14:24:33] "POST /910 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:24:33] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [17/Apr/2026 14:24:36] "POST /910 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:24:36] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [17/Apr/2026 14:24:37] "POST /910 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:24:37] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [17/Apr/2026 14:24:38] "POST /910 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 14:24:38] "GET /static/main.css HTTP/1.1" 304 -
```

## Review page
However, when I tried to load a review, it just didn't load. I waited for 10 minutes, after which I just manually cancelled the page load.

This issue was completely fixed by creating an index on the review_id column of the comment table:
```sql
CREATE INDEX idx_review_id ON comments(review_id);
```

After that simple change, opening a review and paging through the comments was instantaneous:

```
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 13:45:04] "GET /Sample%20artist911/Sample%20album97910/9897909 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 13:45:04] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 13:45:07] "POST /Sample%20artist911/Sample%20album97910/9897909 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 13:45:07] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 13:45:08] "POST /Sample%20artist911/Sample%20album97910/9897909 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 13:45:08] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 13:45:09] "POST /Sample%20artist911/Sample%20album97910/9897909 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 13:45:09] "GET /static/main.css HTTP/1.1" 304 -
```

## Other pages
All other pages seemed snappy enough as is.