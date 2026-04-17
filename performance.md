# Testing the application with large data volumes

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

Looking at an album and paging through the reviews there was similar:

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

Looking at a user page and paging through the user's reviews was a little bit faster with responses just under 0.8 seconds, but the response still felt a bit sluggish:

```
elapsed time: 0.79 s
127.0.0.1 - - [17/Apr/2026 12:37:23] "GET /940 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:37:23] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.79 s
127.0.0.1 - - [17/Apr/2026 12:37:26] "POST /940 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:37:26] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.77 s
127.0.0.1 - - [17/Apr/2026 12:37:28] "POST /940 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:37:28] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.79 s
127.0.0.1 - - [17/Apr/2026 12:37:29] "POST /940 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [17/Apr/2026 12:37:29] "GET /static/main.css HTTP/1.1" 304 -
```