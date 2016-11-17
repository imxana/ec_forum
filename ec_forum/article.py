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

    @app.route('/t/add', methods=['POST'])
    def article_add():
        if request.method != 'POST':
            return jsonify(error.requestError)

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
        if t_title == '':
            return jsonify(error.articleTitleEmpty)
        if t_text == '':
            return jsonify(error.articleTextEmpty)

        '''expr'''
        if not expr.validPack(t_tags):
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
        err,t_id = sqlQ.article_insert(u_id, t_title, t_text, t_tags)
        if err:
            return jsonify(error.serverError)

        '''update userinfo'''
        err,res = sqlQ.id_select(u_id, table='ec_user')
        if err:
            return jsonify(error.serverError)
        u_articles = unpack_id(res[10])
        if t_id not in u_articles[0]:
            u_articles[0].append(t_id)
        if sqlQ.user_update(u_id, {'u_articles':pack_id(u_articles)}):
            return jsonify(error.serverError)

        '''rep'''
        r_type = 'article_add'
        ev = event[r_type]
        # sqlQ.reputation_add(r_type, ec_type, ec_id, ua_id, ua_rep, ub_id, ub_rep)
        err,r_id = sqlQ.reputation_add(r_type, 'article', t_id, u_id, ev[0], u_id, ev[0])
        if err:
            return jsonify(error.serverError)
        '''u_rep'''
        if sqlQ.reputation_user_change(u_id, ev[0]):
            return jsonify(error.serverError)

        return jsonify({'code':'1','t_id':t_id})




    @app.route('/t/query', methods=['POST'])
    def article_query():
        '''query an article by its t_id'''
        if request.method != 'POST':
            return jsonify(error.requestError)
        t_id = request.values.get('t_id','')

        '''empty'''
        if t_id == '':
            return jsonify(error.articleidEmpty)

        '''exist'''
        if not sqlQ.id_search(t_id, table='ec_article'):
            return jsonify(error.articleNotExisted)

        '''database'''
        err,res = sqlQ.id_select(t_id, table='ec_article')
        if err:
            return jsonify(error.serverError)


        return jsonify({
            'code':'1',
            't_id':res[0],
            'u_id':res[1],
            't_title':res[2],
            't_text':res[3],
            't_date':int(res[4].timestamp()),
            't_like':res[5],
            't_comments':res[6],
            't_tags':res[7],
            't_date_latest':int(res[8].timestamp()),
            't_star':res[9]
        })






    @app.route('/t/query_pro', methods=['POST'])
    def article_query_pro():
        if request.method != 'POST':
            return jsonify(error.requestError)
        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        t_id = request.values.get('t_id', '')

        t_star_bool = '0'
        t_recommend_bool = '0'


        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if t_id == '':
            return jsonify(error.articleidEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(t_id, table='ec_article'):
            return jsonify(error.articleNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''Article owner'''
        err,res = sqlQ.id_select(t_id, table='ec_article')
        if err:
            return jsonify(error.serverError)
        ao_id = str(res[1])
        # if res[1] != int(u_id):
        #     return jsonify(error.articleAccess)

        '''select rep'''
        err,rep_event = sqlQ.reputation_select('article_recommend', 'article', t_id, u_id, ao_id)
        if err:
            return jsonify(error.serverError)
        if rep_event != ():
            t_recommend_bool = '1'

        err,rep_event = sqlQ.reputation_select('article_star', 'article', t_id, u_id, ao_id)
        if err:
            return jsonify(error.serverError)
        if rep_event != ():
            t_star_bool = '1'


        return jsonify({
            'code':'1',
            # 't_id':res[0],
            # 'u_id':res[1],
            # 't_title':res[2],
            # 't_text':res[3],
            # 't_date':int(res[4].timestamp()),
            # 't_like':res[5],
            # 't_comments':res[6],
            # 't_tags':res[7],
            # 't_date_latest':int(res[8].timestamp()),
            # 't_star':res[9],
            't_recommend_bool':t_recommend_bool,
            't_star_bool':t_star_bool
        })










    @app.route('/t/del', methods=['POST'])
    def article_delete():
        if request.method != 'POST':
            return jsonify(error.requestError)
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
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(t_id, table='ec_article'):
            return jsonify(error.articleNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''Article owner'''
        err,res = sqlQ.id_select(t_id, table='ec_article')
        if err:
            return jsonify(error.serverError)
        # print('_%s_%s_'%(res[1],u_id), res[1]==int(u_id),type(res[1]),type(u_id))
        if res[1] != int(u_id):
            return jsonify(error.articleAccess)

        '''db'''
        err = sqlQ.id_delete(t_id, table='ec_article')
        if err:
            return jsonify(error.serverError)


        '''update userinfo'''
        err,res = sqlQ.id_select(u_id, table='ec_user')
        if err:
            return jsonify(error.serverError)
        u_articles = unpack_id(res[10])
        if t_id in u_articles[0]:
            u_articles[0].remove(t_id)
        if sqlQ.user_update(u_id, {'u_articles':pack_id(u_articles)}):
            return jsonify(error.serverError)


        '''rep'''
        r_type = 'article_add'
        ev = event[r_type]
        err, rep_event = sqlQ.reputation_select(r_type, 'article', t_id, u_id, u_id)
        if err:
            return jsonify(error.articleNotExisted)
        if sqlQ.id_delete(rep_event[0], table='ec_reputation'):
            return jsonify(error.serverError)
        '''u_rep sub'''
        if sqlQ.reputation_user_change(u_id, -ev[0]):
            return jsonify(error.serverError)

        return jsonify({'code':'1','t_id':t_id})





    @app.route('/t/display', methods=['POST'])
    def article_show():
        if request.method != 'POST':
            return jsonify(error.requestError)

        t_tags = request.values.get('t_tags', '')
        show_count = request.values.get('show_count', '30')

        '''expr'''
        if not expr.validPack(t_tags):
            return jsonify(error.tagNotIllegal)

        t_tags_set = set(unpack_id(t_tags)[0])

        if not set(default_tags).issuperset(t_tags_set):
            return jsonify(error.tagNotExisted)

        '''note: empty is not an error'''
        origin_ids = set()
        if not bool(t_tags_set):
            err,res = sqlQ.article_select_tag()
            for t_tuple in res:
                # 0 t_id int, 5 like int, 9 star int, 8 date, the date type is datetime.datetime, i shock
                t_id,like,star,timestamp = t_tuple[0], int(t_tuple[5]), int(t_tuple[9]), t_tuple[8].timestamp()
                origin_ids.add((t_id,like,star,timestamp))

        for tag in t_tags_set:
            err,res = sqlQ.article_select_tag([tag])
            for t_tuple in res:
                # 0 t_id int, 5 like int, 9 star int, 8 date, the date type is datetime.datetime, i shock
                t_id,like,star,timestamp = t_tuple[0], int(t_tuple[5]), int(t_tuple[9]), t_tuple[8].timestamp()
                origin_ids.add((t_id,like,star,timestamp))

        origin_ids = list(origin_ids)
        show_ids = {0:[],1:[]}
        origin_ids_sorted_by_hot = sorted(origin_ids, key=lambda x: x[1]+x[2], reverse=True)
        origin_ids_sorted_by_date = sorted(origin_ids, key=lambda x: x[3], reverse=True)
        origin_ids_sorted_by_hot = origin_ids_sorted_by_hot[:int(show_count)]
        origin_ids_sorted_by_date = origin_ids_sorted_by_date[:int(show_count)]

        for t_tuple in origin_ids_sorted_by_hot:
            show_ids[0].append(str(t_tuple[0]))
        for t_tuple in origin_ids_sorted_by_date:
            show_ids[1].append(str(t_tuple[0]))
        # for tag in t_tags_set:
        #     err,res = sqlQ.article_select_tag([tag])
        #     for t_tuple in res:
        #         show_ids.add(t_tuple[8])
        #print('ar 184: ', show_ids)
        return jsonify({'code':'1','t_ids':pack_id(show_ids)})













    @app.route('/t/update', methods=['POST'])
    def article_update():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        t_id = request.values.get('t_id', '')
        t_info = {
            't_title': request.values.get('t_title', ''),
            't_text': request.values.get('t_text', ''),
            't_tags': request.values.get('t_tags', ''),
        }

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if t_info['t_title'] == '':
            return jsonify(error.articleTitleEmpty)
        if t_info['t_text'] == '':
            return jsonify(error.articleTextEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(t_id, table='ec_article'):
            return jsonify(error.articleNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''Article owner'''
        err,res = sqlQ.id_select(t_id, table='ec_article')
        if err:
            return jsonify(error.serverError)
        if res[1] != int(u_id):
            return jsonify(error.articleAccess)

        '''db'''
        err = sqlQ.article_update(t_id, t_info, modify=True)
        if err:
            return jsonify(error.serverError)

        return jsonify({'code':'1'})








    @app.route('/t/star', methods=['POST'])
    def article_star():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        t_id = request.values.get('t_id', '')
        u_act = request.values.get('u_act', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if t_id == '':
            return jsonify(error.articleidEmpty)
        if u_act == '':
            return jsonify(error.argsEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(t_id, table='ec_article'):
            return jsonify(error.articleNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)


        '''get article_info'''
        err,res = sqlQ.id_select(t_id, table='ec_article')
        if err:
            return jsonify(error.serverError)
        ub_id,t_star = res[1],res[9]


        '''get rep_info'''
        r_type, ec_type, r_id = 'article_star', 'article', ''
        ev = event[r_type]

        err,rep_event = sqlQ.reputation_select(r_type, ec_type, t_id, u_id, ub_id)
        if err:
            return jsonify(error.serverError)



        if u_act =='1':
            if bool(rep_event):
                return jsonify(error.articleStarAlready)

            '''update userinfo'''
            err,res = sqlQ.id_select(u_id, table='ec_user')
            if err:
                return jsonify(error.serverError)
            u_articles = unpack_id(res[10])
            if t_id in u_articles[1]:
                return jsonify(error.articleStarAlready)
            u_articles[1].append(t_id)
            if sqlQ.user_update(u_id, {'u_articles':pack_id(u_articles)}):
                return jsonify(error.serverError)

            '''add rep_event'''
            if u_id == ub_id:
                err,r_id = sqlQ.reputation_add(r_type, ec_type, t_id, u_id, 0, ub_id, 0)
                if err:
                    return jsonify(error.serverError)
            else:
                err,r_id = sqlQ.reputation_add(r_type, ec_type, t_id, u_id, ev[0], ub_id, ev[1])
                if err:
                    return jsonify(error.serverError)

                '''u_rep'''
                if sqlQ.reputation_user_change(u_id, ev[0]):
                    return jsonify(error.serverError)
                if sqlQ.reputation_user_change(ub_id, ev[1]):
                    return jsonify(error.serverError)
            '''update article_info'''
            if sqlQ.article_update(t_id, {'t_star':int(t_star)+1}):
                return jsonify(error.serverError)

            return jsonify({'code':'1', 'r_id':r_id})

        elif u_act =='0':
            if rep_event == ():
                return jsonify(error.articleNotStar)

            '''update userinfo'''
            err,res = sqlQ.id_select(u_id, table='ec_user')
            if err:
                return jsonify(error.serverError)
            u_articles = unpack_id(res[10])
            if t_id not in u_articles[1]:
                return jsonify(error.articleNotStar)
            u_articles[1].remove(t_id)
            if sqlQ.user_update(u_id, {'u_articles':pack_id(u_articles)}):
                return jsonify(error.serverError)

            '''update t_info'''
            if sqlQ.article_update(t_id, {'t_star':int(t_star)-1}):
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





    @app.route('/t/star_unlink')
    def article_star_unlink():
        '''if star_article be deleted, remove it from my_star'''
        if request.method != 'POST':
            return jsonify(error.requestError)

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
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if sqlQ.id_search(t_id, table='ec_article'):
            return jsonify(error.articleExist)

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
        u_articles = unpack_id(res[10])
        if t_id in u_articles[1]:
            u_articles[1].remove(t_id)
        if sqlQ.user_update(u_id, {'u_articles':pack_id(u_articles)}):
            return jsonify(error.serverError)


        return jsonify({'code':'1'})







    @app.route('/t/recommend', methods=['POST'])
    def article_recommend():
        if request.method != 'POST':
            return jsonify(error.requestError)

        u_id = request.values.get('u_id', '')
        u_psw = request.values.get('u_psw', '')
        t_id = request.values.get('t_id', '')
        u_act = request.values.get('u_act', '')

        '''empty'''
        if u_id == '':
            return jsonify(error.useridEmpty)
        if u_psw == '':
            return jsonify(error.pswEmpty)
        if t_id == '':
            return jsonify(error.articleidEmpty)
        if u_act == '':
            return jsonify(error.argsEmpty)

        '''exist'''
        if not sqlQ.id_search(u_id):
            return jsonify(error.userNotExisted)
        if not sqlQ.id_search(t_id, table='ec_article'):
            return jsonify(error.articleNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.serverError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''get article_info'''
        err,res = sqlQ.id_select(t_id, table='ec_article')
        if err:
            return jsonify(error.serverError)
        ub_id,t_like = res[1],res[5]


        '''get rep_info'''
        r_type, ec_type, r_id = 'article_recommend', 'article', ''
        ev = event[r_type]

        err,rep_event = sqlQ.reputation_select(r_type, ec_type, t_id, u_id, ub_id)
        if err:
            return jsonify(error.serverError)

        '''update rep & article_info'''
        if u_act =='1':
            if bool(rep_event):
                return jsonify(error.articleRecommended)
            if u_id == ub_id:
                err,r_id = sqlQ.reputation_add(r_type, ec_type, t_id, u_id, 0, ub_id, 0)
                if err:
                    return jsonify(error.serverError)
            else:
                err,r_id = sqlQ.reputation_add(r_type, ec_type, t_id, u_id, ev[0], ub_id, ev[1])
                if err:
                    return jsonify(error.serverError)

                '''u_rep'''
                if sqlQ.reputation_user_change(u_id, ev[0]):
                    return jsonify(error.serverError)
                if sqlQ.reputation_user_change(ub_id, ev[1]):
                    return jsonify(error.serverError)

            if sqlQ.article_update(t_id, {'t_like':int(t_like)+1}):
                return jsonify(error.serverError)
            return jsonify({'code':'1', 'r_id':r_id})
        elif u_act =='0':
            if rep_event == ():
                return jsonify(error.articleNotRecommend)
            if sqlQ.article_update(t_id, {'t_like':int(t_like)-1}):
                return jsonify(error.serverError)
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
