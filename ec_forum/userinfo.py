from flask import request,jsonify
import ec_forum.error as error
import ec_forum.sql as sql
from ec_forum.salt import encrypt, decrypt

sqlQ = sql.sqlQ()

def run(app):

    @app.route('/u/query', methods=['POST'])
    def user_query(self):
        if request.method != 'POST':
            return jsonify(error.normalError)
        u_id = request.values.get('u_id', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)

        '''db'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.normalError)
        return jsonify(res)



    @app.route('/u/update', methods=['POST']):
    def user_update(self):
        if request.method != 'POST':
            return jsonify(error.normalError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.normalError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)


        
        # '''err'''
        # if sqlQ.sign_del(u_id):
        #     return jsonify(error.normalError)
