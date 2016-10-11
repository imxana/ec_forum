from flask import request,jsonify
import ec_forum.error as error
from ec_forum.sql import sqlQ
from ec_forum.salt import encrypt, decrypt, secret_key
from ec_forum.id_dealer import pack_id, unpack_id
from ec_forum.public import default_tags
sqlQ = sqlQ()

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
        if t_title == '':
            return jsonify(error.articleTitleEmpty)
        if t_text == '':
            return jsonify(error.articleTextEmpty)

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
        if not sqlQ.userid_search(t_id, table='ec_article'):
            return jsonify(error.articleNotExisted)

        '''database'''
        err,res = sqlQ.article_select(t_id)
        if err:
            return jsonify(error.normalError)


        # print('article.py 65',res)
        # | t_id   | u_id   | t_title | t_text | t_date     | t_like | t_comments | t_tags  |
        # (66831, 981428, 'Title', 'Text', datetime.date(2016, 9, 28), 0, '', 'node.js')
        return jsonify({
            'code':'1',
            't_id':res[0],
            'u_id':res[1],
            't_title':res[2],
            't_text':res[3],
            't_date':res[4],
            't_like':res[5],
            't_comments':res[6],
            't_tags':res[7],
            't_date_latest':res[8],
            't_star':res[9]
        })



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
        if not sqlQ.userid_search(t_id, table='ec_article'):
            return jsonify(error.articleNotExisted)

        '''psw'''
        err,res = sqlQ.signin_select(u_id, method='u_id')
        if err:
            return jsonify(error.normalError)
        decrypt_psw = decrypt(res[2].encode('utf8'))
        if decrypt_psw != u_psw:
            return jsonify(error.pswWrong)

        '''Article owner'''
        err,res = sqlQ.article_select(t_id)
        if err:
            return jsonify(error.normalError)
        # print('_%s_%s_'%(res[1],u_id), res[1]==int(u_id),type(res[1]),type(u_id))
        if res[1] != int(u_id):
            return jsonify(error.articleAccess)

        '''db'''
        err = sqlQ.article_del(t_id)
        if err:
            return jsonify(error.normalError)

        return jsonify({'code':'1','t_id':t_id})





    @app.route('/t/display', methods=['POST'])
    def article_show():
        if request.method != 'POST':
            return jsonify(error.normalError)

        t_tags = request.values.get('t_tags', '')
        show_count = request.values.get('show_count', '30')

        t_tags_set = set(unpack_id(t_tags)[0])

        if not set(default_tags).issuperset(t_tags_set):
            return jsonify(error.tagNotExisted)

        '''note: empty is not an error'''
        show_ids = set()
        for tag in t_tags_set:
            err,res = sqlQ.article_select_tag([tag])
            for t_tuple in res:
                show_ids.add(t_tuple[0])

        return jsonify({'code':'1','t_ids':list(show_ids)[:int(show_count)]})





    @app.route('/t/update', methods=['POST'])
    def article_update():
        return jsonify({'code':'1'})
