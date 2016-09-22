import pymysql
from flask import request,jsonify
import ec_forum.error as error
import ec_forum.sql as sql
import ec_forum.expr as expr

conn = pymysql.Connect(
    host = '127.0.0.1',
    user = 'root',
    passwd = '',
    db = 'test',
    charset = 'utf8'
)

sqlQ = sql.sqlQ()

def run(app):

    @app.route('/sign_up', methods=['POST'])
    def sign_up():
        if request.method != 'POST':
            return jsonify(error.normalError)

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
        err, u_id = sqlQ.signup_insert(u_name, u_email, u_psw)
        if err:
            return jsonify(error.normalError)

        return jsonify({'code':'1','u_id':u_id})






    @app.route('/sign_in', methods=['POST'])
    def sign_in():
        if request.method != 'POST':
            return jsonify(error.normalError)

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
            if method == 'u_name':
                return jsonify(error.usernameExisted)
            if method == 'u_email':
                return jsonify(error.emailExisted)
            return jsonify(error.loginNameNotExisted) 

        err,res = sqlQ.signin_select(u_loginname, u_psw, method)
        if err:
            return jsonify(error.normalError)

        return str(res)



    @app.route('/sign_del', methods=['POST'])
    def sign_del():
        if request.method == 'POST':
            return request.values.get('u_name', '')
        else:
            return jsonify(error.normalError)
