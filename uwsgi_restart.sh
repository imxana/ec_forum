# I don't konw why `service uwsgi restart` doesn't work, so I use `kill` to end them and restart

#pids=`ps -le | grep uwsgi | awk '{print $4}'`

#for i in $pids
#do
    #kill -9 $i
#done

killall -9 uwsgi
supervisorctl restart ec
service nginx restart
