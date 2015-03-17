# Yagra

Yet Another GRAvatar, simple design and quick implementaion.

## Schema of Database

* User

| Field    | Type         | Null | Key | Default | Extra |
|:--------:|:------------:|:----:|:---:|:-------:|:-----:|
| username | varchar(100) | NO   | PRI | NULL    |       |
| password | binary(20)   | YES  |     | NULL    |       |
| avatar   | varchar(50)  | YES  |     | NULL    |       |

* Session

| Field    | Type         | Null | Key | Default | Extra |
|:--------:|:------------:|:----:|:---:|:-------:|:-----:|
| id       | varchar(32)  | NO   | PRI | NULL    |       |
| username | varchar(100) | YES  | UNI | NULL    |       |
| createAt | datetime     | YES  |     | NULL    |       |

## Implementation

Routine of api implementaion.

1. Check whether the parameters is valid. For example: `user_register.py` will check whether `username` contains illegal character, whether the length of `password` is longer enough, etc.

2. Try to create connection of database.

3. CRUD of database

4. Close the db connection, response result to front-end.
