import re

def validEmail(email):
    return bool(re.match(r'^[A-Za-z0-9\_\.]+@[A-Za-z0-9\.]+\.[A-Za-z]{2,4}$',email))

def validName(name):
    return bool(re.match(r'^[a-z][a-z0-9\.]{2,20}$', name))

def validPsw(psw):
    return 6<=len(psw)<=16
