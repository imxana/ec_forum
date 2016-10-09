sudo pip install supervisord
echo_supervisord_conf > /etc/supervisord.conf
echo '[program:ec]
command=python3 /root/workspace/service/ec_forum/app.py
autostart=true
autorestart=true
stdout_logfile=/root/workspace/service/ec_forum/tests/supervisor_stdout.log
stderr_logfile=/root/workspace/service/ec_forum/tests/supervisor_stderr.log
' >> /etc/supervisord.conf

