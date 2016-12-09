from flask import request,jsonify
import ec_forum.error as error
import ec_forum.expr as expr
from ec_forum.sql import sqlQ
from ec_forum.salt import encrypt, decrypt
from ec_forum.id_dealer import pack_id, unpack_id
from ec_forum.public import default_tags
from ec_forum.reputation import event, rule
from config import MyConfig
sqlQ = sqlQ()

def run(app):

    @app.route('/q/add', methods=['POST'])
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
        '''u_rep'''
        if sqlQ.reputation_user_change(u_id, ev[0]):
            return jsonify(error.serverError)

        return jsonify({'code':'1','q_id':q_id})




    @app.route('/q/del', methods=['POST'])
    def question_del():
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        q_id = request.values.get('q_id', '')

        '''empty'''
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

        '''question owner'''
        err,res = sqlQ.id_select(q_id, table='ec_question')
        if err:
            return jsonify(error.serverError)
        # print('_%s_%s_'%(res[1],u_id), res[1]==int(u_id),type(res[1]),type(u_id))
        if res[1] != int(u_id):
            return jsonify(error.questionAccess)

        '''db'''
        err = sqlQ.id_delete(q_id, table='ec_question')
        if err:
            return jsonify(error.serverError)


        '''update userinfo'''
        err,res = sqlQ.id_select(u_id, table='ec_user')
        if err:
            return jsonify(error.serverError)
        u_questions = unpack_id(res[11])
        if q_id in u_questions[0]:
            u_questions[0].remove(q_id)
        if sqlQ.user_update(u_id, {'u_questions':pack_id(u_questions)}):
            return jsonify(error.serverError)


        '''rep'''
        r_type = 'question_add'
        ev = event[r_type]
        err, rep_event = sqlQ.reputation_select(r_type, 'question', q_id, u_id, u_id)
        if err:
            return jsonify(error.questionNotExisted)
        if sqlQ.id_delete(rep_event[0], table='ec_reputation'):
            return jsonify(error.serverError)
        '''u_rep sub'''
        if sqlQ.reputation_user_change(u_id, -ev[0]):
            return jsonify(error.serverError)


        return jsonify({'code':'1','q_id':q_id})




    @app.route('/q/query')
    def question_query():
        '''query a question by its q_id'''
        if request.method != 'GET':
            return jsonify(error.requestError)
        q_id = request.args.get('q_id','')

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







    @app.route('/q/query_pro', methods=['POST'])
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
        #     return jsonify(error.questionAccess)

        '''select rep'''
        err,rep_event = sqlQ.reputation_select('question_like', 'question', q_id, u_id, qo_id)
        if err:
            return jsonify(error.serverError)
        if bool(rep_event):
            q_like_state = '1'

        err,rep_event = sqlQ.reputation_select('question_dislike', 'question', q_id, u_id, qo_id)
        if err:
            return jsonify(error.serverError)
        if bool(rep_event):
            q_like_state = '-1'

        err,rep_event = sqlQ.reputation_select('question_star', 'question', q_id, u_id, qo_id)
        if err:
            return jsonify(error.serverError)
        if bool(rep_event):
            q_star_bool = '1'


        return jsonify({
            'code':'1',
            'q_like_state':q_like_state,
            'q_star_bool':q_star_bool
        })







    @app.route('/q/display')
    def question_display():
        if request.method != 'GET':
            return jsonify(error.requestError)

        q_tags = request.args.get('q_tags', '')
        show_count = request.args.get('show_count', '30')

        '''expr'''
        if not expr.validPack(q_tags):
            return jsonify(error.tagNotIllegal)

        q_tags_set = set(unpack_id(q_tags)[0])

        # note: some tag not existing is ok
        #if not set(default_tags).issuperset(q_tags_set):
        #    return jsonify(error.tagNotExisted)

        '''note: empty is not an error'''
        origin_ids = set()
        for tag in q_tags_set:
            err,res = sqlQ.question_select_tag([tag])
            #note: empty is ok
            # if err:
                # return jsonify(error.serverError)
            for q_tuple in res:
                # 0 q_id int, 6 like int, 12 star int, 5 data, 11 last_date
                q_id,like,star,timestamp = q_tuple[0], int(q_tuple[6]), int(q_tuple[12]), q_tuple[11].timestamp()
                origin_ids.add((q_id,like,star,timestamp))

        origin_ids = list(origin_ids)
        show_ids = {0:[],1:[]}
        origin_ids_sorted_by_hot = sorted(origin_ids, key=lambda x: x[1]+x[2], reverse=True)
        origin_ids_sorted_by_date = sorted(origin_ids, key=lambda x: x[3], reverse=True)
        origin_ids_sorted_by_hot = origin_ids_sorted_by_hot[:int(show_count)]
        origin_ids_sorted_by_date = origin_ids_sorted_by_date[:int(show_count)]

        for q_tuple in origin_ids_sorted_by_hot:
            show_ids[0].append(str(q_tuple[0]))
        for q_tuple in origin_ids_sorted_by_date:
            show_ids[1].append(str(q_tuple[0]))

        return jsonify({'code':'1','q_ids':pack_id(show_ids)})










    @app.route('/q/update', methods=['POST'])
    def question_update():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        q_id = request.values.get('q_id', '')
        q_info = {
            'q_title': request.values.get('q_title', ''),
            'q_text': request.values.get('q_text', ''),
            'q_tags': request.values.get('q_tags', ''),
        }

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if q_id == '':
            return jsonify(error,questionidEmpty)
        if q_info['q_title'] == '':
            return jsonify(error.questionTitleEmpty)
        if q_info['q_text'] == '':
            return jsonify(error.questionTextEmpty)

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
        u_repu = res[6]

        '''Question owner'''
        err,res = sqlQ.id_select(q_id, table='ec_question')
        if err:
            return jsonify(error.serverError)
        if res[1] != int(u_id):
            '''rep request'''
            if u_repu < rule['question_edit']:
                ej = error.reputationNotEnough
                ej['request_repu'] = rule['question_edit']
                ej['now_repu'] = u_repu
                return jsonify(ej)
            # return jsonify(error.questionAccess)


        '''db'''
        err = sqlQ.question_update(q_id, q_info, modify=True)
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1'})









    @app.route('/q/star', methods=['POST'])
    def question_star():
        if request.method != 'POST':
            return jsonify(error.requestError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        q_id = request.values.get('q_id', '')
        u_act = request.values.get('u_act', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if q_id == '':
            return jsonify(error.questionidEmpty)
        if u_act == '':
            return jsonify(error.argsEmpty)

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


        '''get question_info'''
        err,res = sqlQ.id_select(q_id, table='ec_question')
        if err:
            return jsonify(error.serverError)
        ub_id,q_star = res[1],res[12]


        '''get rep_info'''
        r_type, ec_type, r_id = 'question_star', 'question', ''
        ev = event[r_type]

        err,rep_event = sqlQ.reputation_select(r_type, ec_type, q_id, u_id, ub_id)
        if err:
            return jsonify(error.serverError)



        if u_act =='1':
            if bool(rep_event):
                return jsonify(error.questionStarAlready)

            '''update userinfo'''
            err,res = sqlQ.id_select(u_id, table='ec_user')
            if err:
                return jsonify(error.serverError)
            u_questions = unpack_id(res[11])
            if q_id in u_questions[1]:
                return jsonify(error.questionStarAlready)
            u_questions[1].append(q_id)
            if sqlQ.user_update(u_id, {'u_questions':pack_id(u_questions)}):
                return jsonify(error.serverError)

            '''add rep_event'''
            if u_id == ub_id:
                err,r_id = sqlQ.reputation_add(r_type, ec_type, q_id, u_id, 0, ub_id, 0)
                if err:
                    return jsonify(error.serverError)
            else:
                err,r_id = sqlQ.reputation_add(r_type, ec_type, q_id, u_id, ev[0], ub_id, ev[1])
                if err:
                    return jsonify(error.serverError)

                '''u_rep'''
                if sqlQ.reputation_user_change(u_id, ev[0]):
                    return jsonify(error.serverError)
                if sqlQ.reputation_user_change(ub_id, ev[1]):
                    return jsonify(error.serverError)

            '''update question_info'''
            if sqlQ.question_update(q_id, {'q_star':int(q_star)+1}):
                return jsonify(error.serverError)

            return jsonify({'code':'1', 'r_id':r_id})

        elif u_act =='0':
            if not bool(rep_event):
                return jsonify(error.questionNotStar)

            '''update userinfo'''
            err,res = sqlQ.id_select(u_id, table='ec_user')
            if err:
                return jsonify(error.serverError)
            u_questions = unpack_id(res[11])
            if q_id not in u_questions[1]:
                return jsonify(error.questionNotStar)
            u_questions[1].remove(q_id)
            if sqlQ.user_update(u_id, {'u_questions':pack_id(u_questions)}):
                return jsonify(error.serverError)

            '''update q_info'''
            if sqlQ.question_update(q_id, {'q_star':int(q_star)-1}):
                return jsonify(error.serverError)

            '''del rep_event'''
            if sqlQ.id_delete(rep_event[0], table='ec_reputation'):
                return jsonify(error.serverError)

            '''u_rep sub'''
            if sqlQ.reputation_user_change(u_id, -ev[0]):
                return jsonify(error.serverError)
            if sqlQ.reputation_user_change(ub_id, -ev[1]):
                return jsonify(error.serverError)

            return jsonify({'code':'1'})
        else:
            return jsonify(error.argsIllegal)












    @app.route('/q/star_unlink', methods=['POST'])
    def question_star_unlink():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        q_id = request.values.get('q_id', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if q_id == '':
            return jsonify(error.questionidEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if sqlQ.id_search(q_id, table='ec_question'):
            return jsonify(error.questionExist)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)


        '''update userinfo'''
        err,res = sqlQ.id_select(u_id, table='ec_user')
        if err:
            return jsonify(error.serverError)
        u_questions = unpack_id(res[11])
        if q_id in u_questions[1]:
            u_questions[1].remove(q_id)
        if sqlQ.user_update(u_id, {'u_questions':pack_id(u_questions)}):
            return jsonify(error.serverError)


        return jsonify({'code':'1'})







    @app.route('/q/like', methods=['POST'])
    def question_like():
        if request.method != 'POST':
            return jsonify(error.requestError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        q_id = request.values.get('q_id', '')
        u_act = request.values.get('u_act', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if q_id == '':
            return jsonify(error.questionidEmpty)
        if u_act == '':
            return jsonify(error.argsEmpty)

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
        u_repu = res[6]

        '''get question_info'''
        err,res = sqlQ.id_select(q_id, table='ec_question')
        if err:
            return jsonify(error.serverError)
        ub_id,q_like = res[1],res[6]


        '''get rep_info'''
        r_type, r_type2, ec_type, r_id = 'question_like', 'question_dislike', 'question', ''
        ev,ev2 = event[r_type],event[r_type2]

        err,rep_event = sqlQ.reputation_select(r_type, ec_type, q_id, u_id, ub_id)
        if err:
            return jsonify(error.serverError)
        err,rep_event2 = sqlQ.reputation_select(r_type2, ec_type, q_id, u_id, ub_id)
        if err:
            return jsonify(error.serverError)


        '''update rep & question_info'''
        if u_act =='1':
            if bool(rep_event):
                return jsonify(error.questionLikeAlready)
            if u_id == ub_id:
                return jsonify(error.questionSelfAction)
            '''rep request'''
            if not MyConfig.TESTING and u_repu < rule[r_type]:
                ej = error.reputationNotEnough
                ej['request_repu'] = rule[r_type]
                ej['now_repu'] = u_repu
                return jsonify(ej)
            '''if dislike, del it'''
            err,r_id = sqlQ.reputation_add(r_type, ec_type, q_id, u_id, ev[0], ub_id, ev[1])
            if err:
                return jsonify(error.serverError)

            '''u_rep'''
            if sqlQ.reputation_user_change(u_id, ev[0]):
                return jsonify(error.serverError)
            if sqlQ.reputation_user_change(ub_id, ev[1]):
                return jsonify(error.serverError)

            if sqlQ.question_update(q_id, {'q_like':int(q_like)-1}):
                return jsonify(error.serverError)
            if bool(rep_event2):
                if sqlQ.id_delete(rep_event2[0], table='ec_reputation'):
                    return jsonify(error.serverError)
                if sqlQ.question_update(q_id, {'q_like':int(q_like)+1}):
                    return jsonify(error.serverError)
                '''u_rep'''
                if sqlQ.reputation_user_change(u_id, -ev2[0]):
                    return jsonify(error.serverError)
                if sqlQ.reputation_user_change(ub_id, -ev2[1]):
                    return jsonify(error.serverError)
            return jsonify({'code':'1', 'r_id':r_id})
        elif u_act =='0':
            if bool(rep_event):
                if sqlQ.id_delete(rep_event[0], table='ec_reputation'):
                    return jsonify(error.serverError)
                if sqlQ.question_update(q_id, {'q_like':int(q_like)-1}):
                    return jsonify(error.serverError)
                '''u_rep sub'''
                if sqlQ.reputation_user_change(u_id, -ev[0]):
                    return jsonify(error.serverError)
                if sqlQ.reputation_user_change(ub_id, -ev[1]):
                    return jsonify(error.serverError)
                return jsonify({'code':'1','message':'like cancel'})
            if bool(rep_event2):
                if sqlQ.id_delete(rep_event2[0], table='ec_reputation'):
                    return jsonify(error.serverError)
                if sqlQ.question_update(q_id, {'q_like':int(q_like)+1}):
                    return jsonify(error.serverError)
                '''u_rep sub'''
                if sqlQ.reputation_user_change(u_id, -ev2[0]):
                    return jsonify(error.serverError)
                if sqlQ.reputation_user_change(ub_id, -ev2[1]):
                    return jsonify(error.serverError)
                return jsonify({'code':'1','message':'dislike cancel'})
            return jsonify({'code':'1','message':'nothing happended'})
        elif u_act == '-1':
            if bool(rep_event2):
                return jsonify(error.questionDislikeAlready)
            if u_id == ub_id:
                return jsonify(error.questionSelfAction)
            '''rep request'''
            if not MyConfig.TESTING and u_repu < rule[r_type2]:
                ej = error.reputationNotEnough
                ej['request_repu'] = rule[r_type2]
                ej['now_repu'] = u_repu
                return jsonify(ej)
            '''if like, del it'''
            err,r_id = sqlQ.reputation_add(r_type2, ec_type, q_id, u_id, ev2[0], ub_id, ev2[1])
            if err:
                return jsonify(error.serverError)

            '''u_rep'''
            if sqlQ.reputation_user_change(u_id, ev2[0]):
                return jsonify(error.serverError)
            if sqlQ.reputation_user_change(ub_id, ev2[1]):
                return jsonify(error.serverError)
            if sqlQ.question_update(q_id, {'q_like':int(q_like)-1}):
                return jsonify(error.serverError)
            if bool(rep_event):
                if sqlQ.id_delete(rep_event[0], table='ec_reputation'):
                    return jsonify(error.serverError)
                if sqlQ.question_update(q_id, {'q_like':int(q_like)+1}):
                    return jsonify(error.serverError)
                '''u_rep sub'''
                if sqlQ.reputation_user_change(u_id, -ev[0]):
                    return jsonify(error.serverError)
                if sqlQ.reputation_user_change(ub_id, -ev[1]):
                    return jsonify(error.serverError)
            return jsonify({'code':'1', 'r_id':r_id})
        else:
            return jsonify(error.argsIllegal)
