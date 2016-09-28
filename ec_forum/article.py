from flask import request,jsonify
import ec_forum.error as error
import ec_forum.sql as sql
from ec_forum.salt import encrypt, decrypt

sqlQ = sql.sqlQ()

def run(app):

    @app.route('/t/add', methods=['POST'])
    def article_add():
        if request.method != 'POST':
            return jsonify(error.normalError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        t_title = request.values.get('t_title', '')
        t_text = request.values.get('t_text', '')
        t_tags = request.values.get('t_tags', '')

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

        err,t_id = sqlQ.article_insert(u_id, u_psw, t_title, t_text, t_tags)
        if err:
            return jsonify(error.normalError)

        return jsonify({'code':'1','t_id':t_id})


    @app.route('/t/query', methods=['POST'])
    def article_query():
        '''query an article by its t_id'''
        if request.method != 'POST':
            return jsonify(error.normalError)
        t_id = request.values.get('t_id','')

        '''empty'''
        if t_id == '':
            return jsonify(error.articleidEmpty)

        '''exist'''
        if not sqlQ.userid_search(t_id, table='ec_article')
            return jsonify(error.articleNotExisted)

        err,res = sqlQ.article_select(t_id)
        if err:
            return jsonify(error.normalError)

        return json(res)



    @app.route('/t/del', methods=['POST'])
    def article_delete():
        if request.method != 'POST':
            return jsonify(error.normalError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        t_id = request.values.get('t_id', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if t_id == '':
            return jsonify(error.articleidEmpty)

        '''exist'''
        if not sqlQ.userid_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.userid_search(t_id, table='ec_article')
            return jsonify(error.articleNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.normalError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        # wait query done...
        # err,t_id = sqlQ.article_insert(u_id, u_psw, t_title, t_text, t_tags)
        # if err:
        #     return jsonify(error.normalError)
