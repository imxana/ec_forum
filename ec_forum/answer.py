from flask import request,jsonify
import ec_forum.error as error
import ec_forum.expr as expr
from ec_forum.sql import sqlQ
from ec_forum.salt import encrypt, decrypt
from ec_forum.id_dealer import pack_id, unpack_id, gmt_to_timestamp
from ec_forum.public import default_tags
from ec_forum.reputation import event, rule
from config import MyConfig

sqlQ = sqlQ()

def run(app):

    @app.route('/a/add')
    def answer_add():
        if request.method != 'POST':
            return jsonify(error.requestError)
        
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        q_id = request.values.get('q_id', '')
        a_text = request.values.get('a_text', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if a_text == '':
            return jsonify(error.answerTextEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)

        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''db'''
        err,a_id = sqlQ.answer_insert(self, q_id, u_id, a_text)
        if err:
            return jsonify(error.serverError)

        '''update userinfo'''
        err,res = sqlQ.id_select(u_id, table='ec_user')
        if err:
            return jsonify(error.serverError)
        u_answers = unpack_id(res[12])
        if a_id not in u_answers[0]:
            u_answers[0].append(a_id)
        if sqlQ.user_update(u_id, {'u_answers':pack_id(u_answers)}):
            return jsonify(error.serverError)

        '''rep'''
        r_type = 'answer_add'
        ev = event[r_type]
        err,r_id = sqlQ.reputation_add(r_type, 'answer', a_id, u_id, ev[0], u_id, ev[0])
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1','a_id':a_id})

