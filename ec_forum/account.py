import pymysql
from flask import request,jsonify
import ec_forum.error as error
import ec_forum.db as db

conn = pymysql.Connect(
    host = '127.0.0.1',

    user = 'root',
    passwd = '',
    db = 'test',
    charset = 'utf8'
)

sqlQ = db.sqlQ()

def run(app):

    @app.route('/sign_up', methods=['POST'])
    def sign_up():
        if request.method == 'POST':
            u_name = request.values.get('u_name', '')
            if u_name != '':
                u_psw = request.values.get('u_psw', '')
                if u_psw != '':
                    u_email = request.values.get('u_email', '')
                    if sqlQ.signup_select('name'):
                        if db.signup_insert(u_name, u_psw, u_email):
                           return jsonify({
                               'code':'1',
                               'u_id':''
                               })
                    else:
                        return jsonify(error.usernameExisted)
                    # Todo:
                    # return jsonify({
                    #     'u_name':u_name,
                    #     'u_psw':u_psw,
                    #     'u_email':u_email
                    #     })
                else:
                    return jsonify(error.pswEmpty)
            else:
                return jsonify(error.usernameEmpty)
        else:
            return jsonify(error.normalError)

    @app.route('/sign_in', methods=['POST'])
    def sign_in():
        if request.method == 'POST':
            u_name = request.values.get('u_name', '')
            u_email == request.values.get('u_email', '')
            if u_name != '':
                return 'si_name'
            elif u_name != '':
                return 'si_email'
            else:
                return jsonify(error.loginNameEmpty)

        else:
            return jsonify(error.normalError)

    @app.route('/sign_del', methods=['POST'])
    def sign_del():
        if request.method == 'POST':
            return request.values.get('u_name', '')
        else:
            return jsonify(error.normalError)
