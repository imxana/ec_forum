from flask import request,jsonify
import ec_forum.error as error
import ec_forum.sql as sql
from ec_forum.salt import encrypt, decrypt

sqlQ = sql.sqlQ()

def run(app):

    @app.route('/u/query', methods=['POST'])
    def user_query():
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

        return jsonify({
            # 'u_id':res[0],
            'u_name':res[1],
            # 'u_psw':res[2],
            'u_email':res[3],
            # 'u_email_confirm':res[4],
            'u_level':res[5],
            'u_reputation':res[6],
            'u_realname':res[7],
            'u_blog':res[8],
            'u_github':res[9],
            'u_articles':res[10],
            'u_questions':res[11],
            'u_answers':res[12],
            'u_watchusers':res[13],
            'u_tags':res[14]
        })



    @app.route('/u/update', methods=['POST'])
    #self, uid, psw, rn, bl, gh, waus, tags)
    def user_update():
        if request.method != 'POST':
            return jsonify(error.normalError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        u_info = {
            'u_realname':request.values.get('u_realname',''),
            'u_blog':request.values.get('u_blog',''),
            'u_github':request.values.get('u_github',''),
            'u_watchusers':request.values.get('u_watchusers',''),
            'u_tags':request.values.get('u_tags',''),
        }
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

        err = sqlQ.user_update(u_id, u_info)
        if err:
            return jsonify(normalError)

        return jsonify({'code':'1','u_id':u_id})
