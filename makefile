run:
	python3 app.py
su:
	@curl -d 'u_name=Ayase&u_psw=222222&u_email=2@2.com' 'http://localhost:5000/sign_up'
si:
	@curl -d 'u_loginname=Ayase&u_psw=222222' 'http://localhost:5000/sign_in'
sie:
	@curl -d 'u_loginname=2@2.com&u_psw=222222' 'http://localhost:5000/sign_in'
sd:
	@curl -d 'u_id=575504&u_psw=222222' 'http://localhost:5000/sign_del'
