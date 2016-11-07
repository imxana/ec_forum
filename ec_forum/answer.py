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





    @app.route('/a/query', methods=['POST'])
    def answer_query():
        '''query a answer by its a_id'''
        if request.method != 'POST':
            return jsonify(error.requestError)
        a_id = request.values.get('a_id','')

        '''empty'''
        if a_id == '':
            return jsonify(error.answeridEmpty)

        '''exist'''
        if not sqlQ.id_search(a_id, table='ec_answer'):
            return jsonify(error.answerNotExisted)

        '''database'''
        err,res = sqlQ.id_select(a_id, table='ec_answer')
        if err:
            return jsonify(error.serverError)


        return jsonify({
            'code':'1',
            'a_id':res[0],
            'u_id':res[1],
            'a_text':res[2],
            'a_date':int(res[3].timestamp()),
            'a_like':res[4],
            'a_comments':res[5],
            'a_star':res[6]
        })

        
    @app.route('/a/query_pro', methods=['POST'])
    def answer_query_pro():
        if request.method != 'POST':
            return jsonify(error.requestError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        a_id = request.values.get('a_id', '')
        a_star_bool = '0'
        a_like_state = '0'

        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if a_id == '':
            return jsonify(error.answeridEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(a_id, table='ec_answer'):
            return jsonify(error.answerNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''answer owner'''
        err,res = sqlQ.id_select(a_id, table='ec_answer')
        if err:
            return jsonify(error.serverError)
        ao_id = str(res[1])
        # if res[1] != int(u_id):
        #     return jsonify(error.answerAccess)

        '''select rep'''
        err,rep_event = sqlQ.reputation_select('answer_like', 'answer', a_id, u_id, ao_id)
        if err:
            return jsonify(error.serverError)
        if bool(rep_event):
            a_like_state = '1'

        err,rep_event = sqlQ.reputation_select('answer_dislike', 'answer', a_id, u_id, ao_id)
        if err:
            return jsonify(error.serverError)
        if bool(rep_event):
            a_like_state = '-1'

        err,rep_event = sqlQ.reputation_select('answer_star', 'answer', a_id, u_id, ao_id)
        if err:
            return jsonify(error.serverError)
        if bool(rep_event):
            a_star_bool = '1'


        return jsonify({
            'code':'1',
            'a_like_state':a_like_state,
            'a_star_bool':a_star_bool
        })

 





    @app.route('/a/del', methods=['POST'])
    def answer_del():
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        a_id = request.values.get('a_id', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if a_id == '':
            return jsonify(error.answeridEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(a_id, table='ec_answer'):
            return jsonify(error.answerNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''answer owner'''
        err,res = sqlQ.id_select(a_id, table='ec_answer')
        if err:
            return jsonify(error.serverError)
        if res[1] != int(u_id):
            return jsonify(error.answerAccess)

        '''db'''
        err = sqlQ.id_delete(a_id, table='ec_answer')
        if err:
            return jsonify(error.serverError)


        '''update userinfo'''
        err,res = sqlQ.id_select(u_id, table='ec_user')
        if err:
            return jsonify(error.serverError)
        u_answers = unpack_id(res[12])
        if a_id in u_answers[0]:
            u_answers[0].remove(a_id)
        if sqlQ.user_update(u_id, {'u_answers':pack_id(u_answers)}):
            return jsonify(error.serverError)


        '''rep'''
        err, rep_event = sqlQ.reputation_select('answer_add', 'answer', a_id, u_id, u_id)
        if err:
            return jsonify(error.answerNotExisted)
        if sqlQ.id_delete(rep_event[0], table='ec_reputation'):
            return jsonify(error.serverError)

        return jsonify({'code':'1','a_id':a_id})






   
    @app.route('/q/update', methods=['POST'])    
    def answer_update():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        a_id = request.values.get('a_id', '')
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
        if not sqlQ.id_search(a_id, table='ec_answer'):
            return jsonify(error.answerNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''answer owner'''
        err,res = sqlQ.id_select(a_id, table='ec_answer')
        if err:
            return jsonify(error.serverError)
        if res[1] != int(u_id):
            return jsonify(error.answerAccess)

        '''db'''
        err = sqlQ.answer_update(a_id, {'a_text':a_text}, modify=True)
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1'})

  



