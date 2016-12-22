## Experimental_Class_Forum Backend

Python3+Flask+Mysql, A forum of experimental class. ;)

### quick start

install denpendences:

    pip3 install -r requirements.txt

use `doc/schema.sql` to init your mysql database.

test env:
    
    python3 unit_test.py

run server:

    python3 app.py

### deploy

Nginx+uWSGI+supervisor to deploy would be strongly recommended.

read `doc/server_init.sh` as an example.

when it's done, exec it to start:

    uwsgi ./uwsgi.ini 

and to restart:

    ./uwsgi_restart.sh

### global config



