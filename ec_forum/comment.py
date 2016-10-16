from flask import request,jsonify
import ec_forum.error as error
import ec_forum.sql as sql
import ec_forum.expr as expr
from ec_forum.salt import encrypt, decrypt
from ec_forum.id_dealer import pack_id, unpack_id

def run(app):

    @app.route('/c/add', methods=['POST'])
    def coment_add():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        ec_type = request.values.get('ec_type', '')
        ec_id = request.values.get('ec_id', '')
        u_psw = request.values.get('u_psw', '')
        c_text = request.values.get('t_text', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if c_text == '':
            return jsonify(error.commentTextEmpty)
        if ec_id == '':
            return jsonify(error.argsEmpty)

        '''legal'''
        if ec_type not in ('article','question','answer'):
            return jsonify(error.argsIllegal)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.userid_search(ec_id, table='ec_'+ec_type):
            return jsonify(error.commentEventNotExsited)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''db'''
        err,c_id = sqlQ.comment_insert(ec_type, ec_id, u_id, c_text)
        if err:
            return jsonify(error.serverError)

        'todo: and comment id to event["comments"]'

        return jsonify({'code':'1','c_id':c_id})




    @app.route('/c/del', methods=['POST'])
    def article_delete():
        if request.method != 'POST':
            return jsonify(error.requestError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        c_id = request.values.get('t_id', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if c_id == '':
            return jsonify(error.commentidEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.userid_search(t_id, table='ec_comment'):
            return jsonify(error.articleNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''Comment owner'''
        err,res = sqlQ.article_select(t_id)
        if err:
            return jsonify(error.serverError)
        # print('_%s_%s_'%(res[1],u_id), res[1]==int(u_id),type(res[1]),type(u_id))
        if res[1] != int(u_id):
            return jsonify(error.articleAccess)

        '''db'''
        err = sqlQ.id_delete(c_id, table='ec_comment')
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1','t_id':t_id})




    @app.route('/c/l', methods=['POST'])
    def coment_l():
        return 'fuck'
