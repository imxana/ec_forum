# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet

# The origin salt must be safe
orgin_salt = b'8YzsWooy9nWurNur7L3Nj3PJDLfXkWg2UkfJ8VnW4Gc='

def gene_key():
    return Fernet.generate_key()

def encrypt(text, salt):
    return Fernet(salt).encrypt(text.encode('utf-8'))

def decrypt(encrypted_text, salt):
    return str(Fernet(salt).decrypt(encrypted_text), encoding='utf-8')

# test..
if __name__ == '__main__':
    origin_test = 'kangyuh放到ao'
    print ('origin_test: %s' % origin_test)
    encrypted_text = encrypt(origin_test, orgin_salt)
    print ('encrypted_text: %s' % encrypted_text)
    decrypt_text = decrypt(encrypted_text, orgin_salt)
    print ('decrypt_text: %s' % decrypt_text)
