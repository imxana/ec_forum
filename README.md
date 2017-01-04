## Experimental_Class_Forum Backend

Python3 + Flask + Mysql, A forum of experimental class. ;)

### Quick start

install denpendences:

    pip3 install -r requirements.txt

use `doc/schema.sql` to init your mysql database.

test env:
    
    python3 unit_test.py

run server:

    python3 app.py

### Deploy

Nginx + uWSGI + supervisor to deploy Flask application would be strongly recommended.

read `doc/server_init.sh` as an example.

when it's done, exec it to start:

    uwsgi ./uwsgi.ini 

and to restart:

    ./uwsgi_restart.sh

### Global config

open the `config.py` file, `USRENAME` and `PASSWORD` are for the mysql user account, default value `root` and null. if you don't want to connect mysql by localhost, locate the `mysqld.sock` file and set it to the `UNIX_SOCKET`.

### Component

* [Frontend](https://github.com/yuxlan/forum) by [yuxlan](https://github.com/yuxlan) 

* [Backend](https://github.com/imxana/ec_forum) by [imxana](https://github.com/imxana)

### LICENSE

MIT

