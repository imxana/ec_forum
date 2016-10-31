from flask import request,jsonify
import ec_forum.error as error
import ec_forum.expr as expr
from ec_forum.sql import sqlQ
from ec_forum.salt import encrypt, decrypt
from ec_forum.id_dealer import pack_id, unpack_id
from ec_forum.public import default_tags

sqlQ = sqlQ()

def run(app):

    @app.route('/q/add')
    def question_add():
        if request.method != 'POST':
            return jsonify(error.requestError)
        
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        q_title = request.values.get('q_title', '')
        q_text = request.values.get('q_text', '')
        q_tags = request.values.get('q_tags', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if q_title == '':
            return jsonify(error.questionTitleEmpty)
        if q_text == '':
            return jsonify(error.questionTextEmpty)

        '''expr'''
        if not expr.validPack(q_tags):
            return jsonify(error.tagNotIllegal)

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
        err,q_id = sqlQ.question_insert(u_id, q_title, q_tags, q_text)
        if err:
            return jsonify(error.serverError)

        '''update userinfo'''
        err,res = sqlQ.id_select(u_id, table='ec_user')
        if err:
            return jsonify(error.serverError)
        u_questions = unpack_id(res[11])
        if q_id not in u_questions[0]:
            u_questions[0].append(q_id)
        if sqlQ.user_update(u_id, {'u_questions':pack_id(u_questions)}):
            return jsonify(error.serverError)

        '''rep'''
        r_type = 'question_add'
        ev = event[r_type]
        err,r_id = sqlQ.reputation_add(r_type, 'question', q_id, u_id, ev[0], u_id, ev[0])
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1','q_id':q_id})





    @app.route('/q/query', methods=['POST'])
    def question_query():
        '''query a question by its q_id'''
        if request.method != 'POST':
            return jsonify(error.requestError)
        q_id = request.values.get('q_id','')

        '''empty'''
        if q_id == '':
            return jsonify(error.questionidEmpty)

        '''exist'''
        if not sqlQ.id_search(q_id, table='ec_question'):
            return jsonify(error.questionNotExisted)

        '''database'''
        err,res = sqlQ.id_select(q_id, table='ec_question')
        if err:
            return jsonify(error.serverError)


        return jsonify({
            'code':'1',
            'q_id':res[0],
            'u_id':res[1],
            'q_title':res[2],
            'q_tags':res[3],
            'q_text':res[4],
            'q_date':int(res[5].timestamp()),
            'q_like':res[6],
            'q_close':res[7],
            'q_report':res[8],
            'q_answers':res[9],
            'q_comments':res[10],
            'q_date_latest':int(res[11].timestamp()),
            'q_star':res[12]
        })

        


    @app.route('/q/query_pro', methods=['GET'])
    def question_query_pro():
        if request.method != 'POST':
            return jsonify(error.requestError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        q_id = request.values.get('q_id', '')
        q_star_bool = '0'
        q_like_state = '0'

        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if q_id == '':
            return jsonify(error.questionidEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(q_id, table='ec_question'):
            return jsonify(error.questionNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''Question owner'''
        err,res = sqlQ.id_select(q_id, table='ec_question')
        if err:
            return jsonify(error.serverError)
        qo_id = str(res[1])
        # if res[1] != int(u_id):
        #     return jsonify(error.articleAccess)

        '''select rep'''
        err,rep_event = sqlQ.reputation_select('question_like', 'question', q_id, u_id, qo_id)
        if err:
            return jsonify(error.serverError)
        if rep_event != ():
            q_like_state = '1'

        err,rep_event = sqlQ.reputation_select('question_dislike', 'question', q_id, u_id, qo_id)
        if err:
            return jsonify(error.serverError)
        if rep_event != ():
            q_like_state = '-1'

        err,rep_event = sqlQ.reputation_select('question_star', 'question', q_id, u_id, qo_id)
        if err:
            return jsonify(error.serverError)
        if rep_event != ():
            q_star_bool = '1'


        return jsonify({
            'code':'1',
            'q_like_state':q_like_state,
            'q_star_bool':q_star_bool
        })








    if request.method != 'POST':
            return jsonify(error.requestError)
        
        return jsonify({'code':'1'})





    @app.route('/q/display', methods=['POST'])
    def question_display():
        if request.method != 'POST':
            return jsonify(error.requestError)

        return jsonify({'code':'1'})




    @app.route('/q/del', methods=['POST'])
    def question_del():

        return jsonify({'code':'1'})





    @app.route('/q/update', methods=['POST'])    
    def question_update():
        if request.method != 'POST':
            return jsonify(error.requestError)

        return jsonify({'code':'1'})







    @app.route('/q/star', methods=['POST'])
    def question_star():
        if request.method != 'POST':
            return jsonify(error.requestError)
        return jsonify({'code':'1'})




    @app.route('/q/star_unlink', methods=['POST'])
    def question_star_unlink():
        if request.method != 'POST':
            return jsonify(error.requestError)
        return jsonify({'code':'1'})





    @app.route('/q/like', methods=['POST'])
    def question_like():
        if request.method != 'POST':
            return jsonify(error.requestError)
        return jsonify({'code':'1'})




    

