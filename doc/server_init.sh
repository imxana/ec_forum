# the script to init your ubuntu server, just for reference
# Don't run this script! Though it is executable.

# install supervisord
sudo pip install supervisord

# set supervisord args
sv_conf_path=/etc/supervisor.conf

if [ ! -e $sv_conf_path ]; then
    echo_supervisord_conf > $sv_conf_path
fi

echo '[program:ec]
command=uwsgi /root/workspace/service/ec_forum/uwsgi.ini
autostart=true
autorestart=true
stdout_logfile=/root/workspace/service/ec_forum/logs/uwsgi_stdout.log
stderr_logfile=/root/workspace/service/ec_forum/logs/uwsgi_stderr.log
' >> $sv_conf_path


# set nginx args
nginx_conf_path=/etc/nginx/conf.d

if [ ! -d $nginx_conf_path  ]; then
    mkdir -p $nginx_conf_path
fi

echo 'server {
    listen 5000;

    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:3032;
        #uwsgi_param UWSGI_PYHOME /usr/bin;
        uwsgi_param UWSGI_CHDIR /root/workspace/service/ec_forum;
        uwsgi_param UWSGI_SCRIPT app:app;
        uwsgi_read_timeout 100;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

}' > $nginx_conf_path/ec.conf

