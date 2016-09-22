# -*- coding: utf-8 -*-
from flask import jsonify
from cryptography.fernet import Fernet

# must be safe
origin_salt = b'8YzsWooy9nWurNur7L3Nj3PJDLfXkWg2UkfJ8VnW4Gc='
secret_key = 'BnUcbCUHZj3lzrdHutfAI5cRCBLzBY3JIAIxt2ZWUz8='

def gene_key():
    return Fernet.generate_key()

def encrypt(text, salt=origin_salt):
    return Fernet(salt).encrypt(text.encode('utf-8'))

def decrypt(encrypted_text, salt=origin_salt):
    return str(Fernet(salt).decrypt(encrypted_text), encoding='utf-8')

def run(app):
    @app.route('/safe/secret_key')
    def get_secret_key():
        return jsonify({'secret_key':secret_key})

# test..
if __name__ == '__main__':
    origin_test = 'kangyuhao好帅'
    print ('origin_test: %s' % origin_test)
    encrypted_text = encrypt(origin_test, origin_salt)
    print ('encrypted_text: %s' % str(encrypted_text, encoding='utf-8'))
    decrypt_text = decrypt(encrypted_text, origin_salt)
    print ('decrypt_text: %s' % decrypt_text)
