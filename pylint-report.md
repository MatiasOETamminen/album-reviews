# Pylint report

Pylint gives the following output:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:66:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:81:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:88:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:94:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:99:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:143:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:177:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:206:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:236:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:274:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:299:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:341:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:363:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:377:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:398:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:11:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:22:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:28:4: C0103: Constant name "username" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:29:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:33:4: C0103: Constant name "name" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:34:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:38:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:42:4: C0103: Constant name "name" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:45:4: C0103: Constant name "songlist" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:55:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:58:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:64:4: C0103: Constant name "album_name" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:66:4: C0103: Constant name "content" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:68:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:76:4: C0103: Constant name "content" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:77:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module services
services.py:1:0: C0114: Missing module docstring (missing-module-docstring)
services.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:50:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:73:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:91:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:99:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:108:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:114:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:119:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:128:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:134:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:139:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:145:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:152:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:171:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:177:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:181:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:192:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:198:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:203:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:216:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:223:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:228:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:233:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:244:0: C0116: Missing function or method docstring (missing-function-docstring)
services.py:250:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.56/10 (previous run: 8.55/10, +0.02)
```
## Docstrings

Most of the lines are reports about missing docstrings:
```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
```
Writing docstrings is outside the scope of this course, so a conscious decision has been made not to write them.

## Dangerous default value

There are two instances of warnings about a dangerous default value:
```
db.py:11:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:22:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```
These warnigns refer to these two functions in the db.py file:
```python
def execute(sql, params=[]):
    con = get_connection()
    with con:
        result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```
```python
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
```
The same empty list object is shared between all the calls of these functions. However, this doesn't create an issue, because there is no code that alters the list.

## Constant name style

There are a handful of comments about constants not being named with the UPPER_CASE naming style:
```
seed.py:28:4: C0103: Constant name "username" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:29:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:33:4: C0103: Constant name "name" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:34:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:38:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:42:4: C0103: Constant name "name" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:45:4: C0103: Constant name "songlist" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:55:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:58:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:64:4: C0103: Constant name "album_name" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:66:4: C0103: Constant name "content" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:68:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:76:4: C0103: Constant name "content" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:77:4: C0103: Constant name "sql" doesn't conform to UPPER_CASE naming style (invalid-name)
```
These all refer to the variables inside the loops in the seed.py file, e.g.:
```python
for i in range(1, USER_COUNT + 1):
    password = generate_password_hash("1")
    username = "Sample" + str(i)
    sql = """INSERT INTO users (username, password_hash) VALUES (?, ?);"""
    db.execute(sql, [username, password])
```
Pylint seems to consider the username and the sql (and similar variables in other similar loops) as constants. However, I think it is more consistent to write them in lowercase because similar sqlite operation variables inside the services.py are also written in lowercase. Pylint doesn't mention those, most likely because those are inside functions.