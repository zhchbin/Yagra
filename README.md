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
    $ sudo apt-get install mysql-server libmysqlclient-dev -y
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


* Clone Yagra

    ```bash
    $ git clone https://github.com/zhchbin/Yagra.git /var/www/Yagra
    $ chown -R www-data:www-data /var/www/Yagra
    $ cd /var/www/Yagra/cgi-bin
    $ cp config.example.py config.py
    ```

    Fill your database configuration and avatar directory path in `config.py`.

* Apache2

    ```bash
    $ sudo apt-get install apache2 -y
    ```
    
    Config of `/etc/apache2/sites-available/000-default.conf`
    
    ```
    <VirtualHost *:80>
      # The ServerName directive sets the request scheme, hostname and port that
      # the server uses to identify itself. This is used when creating
      # redirection URLs. In the context of virtual hosts, the ServerName
      # specifies what hostname must appear in the request's Host: header to
      # match this virtual host. For the default virtual host (this file) this
      # value is not decisive as it is used as a last resort host regardless.
      # However, you must set it for any further virtual host explicitly.
      #ServerName www.example.com
    
      ServerAdmin webmaster@localhost
      DocumentRoot /var/www/Yagra/static
      ScriptAlias /cgi-bin/ /var/www/Yagra/cgi-bin/
      <Directory "/var/www/Yagra/cgi-bin">
        AllowOverride None
        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
        Require all granted
      </Directory>
    
    
      # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
      # error, crit, alert, emerg.
      # It is also possible to configure the loglevel for particular
      # modules, e.g.
      #LogLevel info ssl:warn
    
      ErrorLog ${APACHE_LOG_DIR}/error.log
      CustomLog ${APACHE_LOG_DIR}/access.log combined
    
      # For most configuration files from conf-available/, which are
      # enabled or disabled at a global level, it is possible to
      # include a line for only one particular virtual host. For example the
      # following line enables the CGI configuration for this host only
      # after it has been globally disabled with "a2disconf".
      #Include conf-available/serve-cgi-bin.conf
    </VirtualHost>
    
    # vim: syntax=apache ts=4 sw=4 sts=4 sr noet
    ```
    
    ```bash
    $ ln -s /etc/apache2/mods-available/cgid.load /etc/apache2/mods-enabled/
    $ ln -s /etc/apache2/mods-available/cgid.conf /etc/apache2/mods-enabled/
    $ service apache2 reload
    ```
