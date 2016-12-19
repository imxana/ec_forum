# I don't konw why `service uwsgi restart` doesn't work, so I use `kill` to end them and restart
#pids=`ps -le | grep uwsgi | awk '{print $4}'`|xargs kill -9


killall -9 uwsgi
# wait

# note: autorestart:true
# supervisorctl start ec
# wait

# nginx no need restart
#service nginx restart

