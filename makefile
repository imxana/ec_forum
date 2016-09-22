su:
	@curl -d 'u_name=Ayase&u_psw=222222&u_email=2@2.com' 'http://localhost:5000/sign_up'
si:
	@curl -d 'u_loginname=Ayase&u_psw=222222' 'http://localhost:5000/sign_in'
