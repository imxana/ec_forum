su:
	@curl -d 'u_name=Ayase&u_psw=' 'http://localhost:5000/sign_up'
sug:
	@curl 'http://localhost:5000/sign_up?u_name=Ayase&gender=f'
