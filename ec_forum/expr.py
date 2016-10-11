import re

'''\d [0-9]'''
'''\w [A-Za-z0-9_]'''
'''\W [^A-Za-z0-9_]'''
def validEmail(email):
    return bool(re.match(r'^[A-Za-z0-9\_\.]+@[A-Za-z0-9\.]+\.[A-Za-z]{2,4}$',email))

def validName(name):
    return bool(re.match(r'^[a-z][a-z0-9\.]{2,20}$', name))

def validPsw(psw):
    return 6<=len(psw)<=16

def validPack(pack_id):
    return bool(re.match(r'^[\u4e00-\u9fa5\w\,\&\.\+\-\#]*$',pack_id))


if __name__ == '__main__':
    test_arr = ['&', '1&', '&a', '2&3,4','32','&,,,&',',&','&,','哈哈','哈&_','&哈哈']
    for i in test_arr:
        print(i,validPack(i))
