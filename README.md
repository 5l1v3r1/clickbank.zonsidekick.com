Install
=======

Step 1:
-------

```
$ cd clickbank.zonsidekick.com
$ git clone git@bitbucket.org:kalkura/clickbank.zonsidekick.com.git .
```

Step 2:
-------

```
$ cd clickbank.zonsidekick.com
$ mkvirtualenv clickbank.zonsidekick.com
$ pip install -r requirements.txt
$ cp settings.py.sample settings.py
$ deactivate
```

Step 3:
-------

```
$ cd clickbank.zonsidekick.com
$ npm install -g bower
$ npm install -g less
$ bower install
```

Step 4:
-------

```
$ cd clickbank.zonsidekick.com
$ mysql -e 'CREATE DATABASE `clickbank.zonsidekick.com`'
$ mysql clickbank.zonsidekick.com < files/0.sql
$ mysql clickbank.zonsidekick.com < files/1.sql
```

Assets
======

```
$ cd clickbank.zonsidekick.com
$ workon clickbank.zonsidekick.com
$ python manager.py assets_
$ deactivate
```
