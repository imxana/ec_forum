from flask import request,jsonify
import ec_forum.error as error
import ec_forum.sql as sql
from ec_forum.salt import encrypt, decrypt
from ec_forum.id_dealer import pack_id, unpack_id
from ec_forum.reputation import event, rule
from config import MyConfig
sqlQ = sql.sqlQ()

def run(app):

    @app.route('/c/add', methods=['POST'])
    def comment_add():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        ec_type = request.values.get('ec_type', '')
        ec_id = request.values.get('ec_id', '')
        c_text = request.values.get('c_text', '')

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
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(ec_id, table='ec_'+ec_type):
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

        '''update event_info'''
        err,res = sqlQ.id_select(ec_id, table='ec_'+ec_type)
        if err:
            return jsonify(error.serverError)
        ub_id = ''

        if ec_type == 'article':
            ub_id = res[1]
            t_comments = unpack_id(res[6])
            if int(c_id) not in t_comments[0]:
                t_comments[0].append(c_id)
            if sqlQ.article_update(ec_id, {'t_comments':pack_id(t_comments)}):
                return jsonify(error.serverError)
        elif ec_type == 'question':
            ub_id = res[1]
            q_comments = unpack_id(res[10])
            if int(c_id) not in q_comments[0]:
                q_comments[0].append(c_id)
            if sqlQ.question_update(ec_id, {'q_comments':pack_id(q_comments)}):
                return jsonify(error.serverError)
        elif ec_type == 'answer':
            ub_id = res[1]
            a_comments = unpack_id(res[5])
            if int(c_id) not in a_comments[0]:
                a_comments[0].append(c_id)
            if sqlQ.answer_update(ec_id, {'a_comments':pack_id(a_comments)}):
               return jsonify(error.serverError)


        '''rep'''
        r_type = 'comment_add'
        ev = event[r_type]
        err,r_id = sqlQ.reputation_add(r_type, ec_type, ec_id, u_id, ev[0], ub_id, ev[1])
        if err:
            return jsonify(error.serverError)
        '''u_rep'''
        if sqlQ.reputation_user_change(u_id, ev[0]):
            return jsonify(error.serverError)
        if sqlQ.reputation_user_change(ub_id, ev[1]):
            return jsonify(error.serverError)

        return jsonify({'code':'1','c_id':c_id})




    @app.route('/c/del', methods=['POST'])
    def comment_delete():
        if request.method != 'POST':
            return jsonify(error.requestError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        c_id = request.values.get('c_id', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if c_id == '':
            return jsonify(error.commentidEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(c_id, table='ec_comment'):
            return jsonify(error.commentNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''query comment event'''
        err,res = sqlQ.id_select(c_id, table='ec_comment')
        if err:
            return jsonify(error.serverError)
        # print('c.py 102: _%s_%s_'%(res[3],u_id), res[3]==int(u_id),type(res[3]),type(u_id))
        ec_type,ec_id,co_id = res[1],res[2],res[3]

        '''ec_event owner'''
        err,res = sqlQ.id_select(ec_id, table='ec_'+ec_type)
        if err:
            return jsonify(error.serverError)
        eo_id = res[1]
        if int(u_id) not in (co_id, eo_id):
            return jsonify(error.commentAccess)

        '''db'''
        err = sqlQ.id_delete(c_id, table='ec_comment')
        if err:
            return jsonify(error.serverError)

        # '''rep'''
        # r_type = 'comment_del'
        # ev = event[r_type]
        # err,r_id = sqlQ.reputation_add(r_type, ec_type, ec_id, u_id, ev[0], eo_id, ev[1])
        # if err:
        #     return jsonify(error.serverError)

        '''rep'''
        err, rep_event = sqlQ.reputation_select('comment_add', ec_type, ec_id, u_id, eo_id)
        if err:
            return jsonify(error.commentNotExisted)
        if sqlQ.id_delete(rep_event[0], table='ec_reputation'):
            return jsonify(error.serverError)
        '''u_rep sub'''
        ev = event['comment_add']
        if sqlQ.reputation_user_change(co_id, -ev[0]):
            return jsonify(error.serverError)
        if sqlQ.reputation_user_change(eo_id, -ev[1]):
            return jsonify(error.serverError)
        return jsonify({'code':'1','c_id':c_id})




    @app.route('/c/query')
    def comment_query():
        '''query a comment by its c_id'''
        if request.method != 'GET':
            return jsonify(error.requestError)
        c_id = request.args.get('c_id','')

        '''empty'''
        if c_id == '':
            return jsonify(error.commentidEmpty)

        '''exist'''
        if not sqlQ.id_search(c_id, table='ec_comment'):
            return jsonify(error.commentNotExisted)

        '''database'''
        err,res = sqlQ.id_select(c_id, table='ec_comment')
        if err:
            return jsonify(error.serverError)

        return jsonify({
            'code':'1',
            'c_id':res[0],
            'ec_type':res[1],
            'ec_id':res[2],
            'u_id':res[3],
            'c_text':res[4],
            'c_date':int(res[5].timestamp()),
            'c_like':res[6],
        })



    @app.route('/c/like', methods=['POST'])
    def comment_like():
        if request.method != 'POST':
            return jsonify(error.requestError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        c_id = request.values.get('c_id', '')
        u_act = request.values.get('u_act', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if c_id == '':
            return jsonify(error.commentidEmpty)
        if u_act == '':
            return jsonify(error.argsEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(c_id, table='ec_comment'):
            return jsonify(error.commentNotExisted)

        '''psw, get repu'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)
        u_repu = res[6]

        '''get comment_info'''
        err,res = sqlQ.id_select(c_id, table='ec_comment')
        if err:
            return jsonify(error.serverError)
        ub_id,c_like = res[3],res[6]


        '''get rep_info'''
        r_type, r_type2, ec_type, r_id = 'comment_like', 'comment_dislike', 'comment', ''
        ev,ev2 = event[r_type],event[r_type2]

        err,rep_event = sqlQ.reputation_select(r_type, ec_type, c_id, u_id, ub_id)
        err2,rep_event2 = sqlQ.reputation_select(r_type2, ec_type, c_id, u_id, ub_id)
        if err and err2:
            return jsonify(error.serverError)


        '''update rep & comment_info'''
        if u_act =='1':
            if bool(rep_event):
                return jsonify(error.commentLikeAlready)
            if u_id == ub_id:
                return jsonify(error.commentSelfAction)
            if not MyConfig.TESTING and u_repu < rule[r_type]:
                ej = error.reputationNotEnough
                ej['request_repu'] = rule[r_type]
                ej['now_repu'] = u_repu
                return jsonify(ej)
            '''if dislike, del it'''
            err,r_id = sqlQ.reputation_add(r_type, ec_type, c_id, u_id, ev[0], ub_id, ev[1])
            if err:
                return jsonify(error.serverError)
            if sqlQ.comment_update(c_id, {'c_like':int(c_like)-1}):
                return jsonify(error.serverError)
            if bool(rep_event2):
                if sqlQ.id_delete(rep_event2[0], table='ec_reputation'):
                    return jsonify(error.serverError)
                if sqlQ.comment_update(c_id, {'c_like':int(c_like)+1}):
                    return jsonify(error.serverError)
            return jsonify({'code':'1', 'r_id':r_id})
        elif u_act =='0':
            if bool(rep_event):
                if sqlQ.id_delete(rep_event[0], table='ec_reputation'):
                    return jsonify(error.serverError)
                if sqlQ.comment_update(c_id, {'c_like':int(c_like)-1}):
                    return jsonify(error.serverError)
                return jsonify({'code':'1','message':'like cancel'})
            if bool(rep_event2):
                if sqlQ.id_delete(rep_event2[0], table='ec_reputation'):
                    return jsonify(error.serverError)
                if sqlQ.comment_update(c_id, {'c_like':int(c_like)+1}):
                    return jsonify(error.serverError)
                return jsonify({'code':'1','message':'dislike cancel'})
            return jsonify({'code':'1','message':'nothing happended'})
        elif u_act == '-1':
            if bool(rep_event2):
                return jsonify(error.commentDislikeAlready)
            if u_id == ub_id:
                return jsonify(error.commentSelfAction)
            if not MyConfig.TESTING and u_repu < rule[r_type2]:
                ej = error.reputationNotEnough
                ej['request_repu'] = rule[r_type2]
                ej['now_repu'] = u_repu
                return jsonify(ej)
            '''if like, del it'''
            err,r_id = sqlQ.reputation_add(r_type2, ec_type, c_id, u_id, ev2[0], ub_id, ev2[1])
            if err:
                return jsonify(error.serverError)
            if sqlQ.comment_update(c_id, {'c_like':int(c_like)-1}):
                return jsonify(error.serverError)
            if bool(rep_event):
                if sqlQ.id_delete(rep_event[0], table='ec_reputation'):
                    return jsonify(error.serverError)
                if sqlQ.comment_update(c_id, {'c_like':int(c_like)+1}):
                    return jsonify(error.serverError)
            return jsonify({'code':'1', 'r_id':r_id})
        else:
            return jsonify(error.argsIllegal)
