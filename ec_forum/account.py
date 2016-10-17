# import pymysql
from flask import request,jsonify
import ec_forum.error as error
import ec_forum.sql as sql
import ec_forum.expr as expr
from ec_forum.salt import encrypt, decrypt

sqlQ = sql.sqlQ()

def run(app):

    @app.route('/sign_up', methods=['POST'])
    def sign_up():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_name = request.values.get('u_name', '').lower()
        u_email = request.values.get('u_email', '')
        u_psw = request.values.get('u_psw', '')

        '''empty'''
        if u_name == '':
            return jsonify(error.usernameEmpty)
        if u_email == '':
            return jsonify(error.emailEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)

        '''formate legal'''
        if not expr.validName(u_name):
            return jsonify(error.usernameIllegal)
        if not expr.validEmail(u_email):
            return jsonify(error.emailIllegal)
        if not expr.validPsw(u_psw):
            return jsonify(error.pswIllegal)


        '''exist'''
        if sqlQ.signup_select(u_name, method='u_name'):
            return jsonify(error.usernameExisted)
        if sqlQ.signup_select(u_email, method='u_email'):
            return jsonify(error.emailExisted)


        '''insert err'''
        encrypt_psw = str(encrypt(u_psw), encoding='utf8')
        err, u_id = sqlQ.signup_insert(u_name, u_email, encrypt_psw)
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1','u_id':u_id})






    @app.route('/sign_in', methods=['POST'])
    def sign_in():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_loginname = request.values.get('u_loginname', '')
        u_psw = request.values.get('u_psw', '')

        '''empty'''
        method = ''
        if u_loginname == '':
            return jsonify(error.loginNameEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)

        '''formate type'''
        if expr.validEmail(u_loginname):
            method = 'u_email'
        elif expr.validName(u_loginname.lower()):
            method = 'u_name'
        else:
            return jsonify(error.loginNameIllegal)

        '''exist'''
        if not sqlQ.signup_select(u_loginname, method=method):
            if method == 'u_email':
                return jsonify(error.emailNotExisted)
            return jsonify(error.userNotExisted)

        # str(encrypt(u_psw), encoding='utf8')
        err,res = sqlQ.signin_select(u_loginname, method)
        if err:
            return jsonify(error.serverError)

        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        return jsonify({
            'code': '1',
            'u_id': res[0],
            'u_name': res[1],
            #'u_psw':res[2],
            'u_email': res[3],
            'u_email_confirm': res[4],
            'u_level': res[5],
            'u_reputation': res[6],
            'u_realname': res[7],
            'u_blog': res[8],
            'u_github': res[9],
            'u_articles': res[10],
            'u_questions': res[11],
            'u_answers': res[12],
            'u_watchusers': res[13],
            'u_tags': res[14],
            'u_intro': res[15],
            })



    @app.route('/safe/sign_del', methods=['POST'])
    def sign_del():
        if request.method != 'POST':
            return jsonify(error.requestError)
        if not app.config['DEBUG']:
            return jsonify(error.methodAbort)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)

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

        '''err'''
        if sqlQ.id_delete(u_id,table='ec_user'):
            return jsonify(error.serverError)

        return jsonify({'code':'1','u_id':u_id})
