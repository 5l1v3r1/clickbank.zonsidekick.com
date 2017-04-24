How to install?
===============

Step 1
------

```
$ cd clickbank.zonsidekick.com
$ git clone git@github.com:mahendrakalkura/clickbank.zonsidekick.com.git .
$ cp settings.py.sample settings.py
```

Step 2
------

```
$ cd clickbank.zonsidekick.com
$ mysql -e 'CREATE DATABASE `clickbank.zonsidekick.com`'
$ mysql clickbank.zonsidekick.com < files/1.sql
```

Step 3
------

```
$ cd clickbank.zonsidekick.com
$ bower install
```

Step 4
------

```
$ cd clickbank.zonsidekick.com
$ mkvirtualenv clickbank.zonsidekick.com
$ pip install -r requirements.txt
$ python manager.py assets_build
$ deactivate
```

How to run?
===========

```
$ cd clickbank.zonsidekick.com
$ workon clickbank.zonsidekick.com
$ python server.py
$ deactivate
```
