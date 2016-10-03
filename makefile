run:
	python3 app.py
test:
	python3 test.py
ssh:
	@ssh root@139.129.24.151
ssh2:
	@ssh root@115.28.16.220
ip:
	@ifconfig | grep "inet " | grep -v 127.0.0.1



su:
	@curl -d 'u_name=Ayase&u_psw=222222&u_email=2@2.com' 'http://localhost:5000/sign_up'
si:
	@curl -d 'u_loginname=Ayase&u_psw=222222' 'http://localhost:5000/sign_in'
sie:
	@curl -d 'u_loginname=2@2.com&u_psw=222222' 'http://localhost:5000/sign_in'
sd:
	@curl -d 'u_id=575504&u_psw=222222' 'http://localhost:5000/sign_del'

