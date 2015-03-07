# Yagra
Yet Another GRAvatar

## Coding Style Check

```bash
$ sudo pip install pep8
$ pep8 cgi-bin
```

## Setup

* MySQL

```bash
$ sudo apt-get install mysql-server libmysqlclient-dev
$ sudo pip install -r requirements.txt
```

Create a new database user and a new database

``` bash
$ mysql -u root -p
Enter Password:
...

mysql> CREATE DATABASE yagra;
mysql> CREATE USER 'yagra_user'@'localhost' IDENTIFIED BY '<user_password>';
mysql> USE yagra;
mysql> GRANT ALL ON yagra.* TO 'yagra_user'@'localhost';
mysql> CREATE TABLE User(username VARCHAR(100) PRIMARY KEY, password BINARY(20), avatar VARCHAR(50));
mysql> CREATE TABLE Session (id VARCHAR(32) PRIMARY KEY, username VARCHAR(100) UNIQUE KEY, createAt DATETIME);
```

## TODO

- [ ] Should we add frequence limitaion of user register/login or use captcha?
