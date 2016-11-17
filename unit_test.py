from flask import json
import unittest
import tempfile
import app as ec
from ec_forum.id_dealer import gene_id
import config

class ECTestCase(unittest.TestCase):

    def setUp(self):
        # ec.app.config['TESTING'] = True
        config.MyConfig = config.DevelopmentConfig()
        self.app = ec.app.test_client()
        self.name = 'a'+gene_id(num=5, letter=True, lower=True)
        self.email = self.name+'@gmail.com'
        self.name2 = 'n'+gene_id(num=5, letter=True, lower=True)
        self.email2 = self.name2+'@gmail.com'
        '''sign_up suc'''
        rv = self.sign_up(self.name,'222222',self.email)
        self.u_id = json.loads(rv.data).get('u_id','')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.sign_up(self.name2,'222222','1401520070@qq.com')
        self.ua_id = json.loads(rv.data).get('u_id','')
        assert '1' == json.loads(rv.data).get('code','')
        '''article_add_suc'''
        rv = self.article_add(self.u_id, '222222', 'What\'s nodejs',
'''Node.js  is a set of libraries for JavaScript which allows it to be used outside of the
browser. It is primarily focused on creating simple, easy to build network clients  and
servers.''', 'node.js')
        self.t_id = json.loads(rv.data).get('t_id','')
        assert '1' == json.loads(rv.data).get('code','')


    def tearDown(self):
        '''article_del_suc'''
        rv = self.article_del(self.u_id, '222222', self.t_id)
        assert '1' == json.loads(rv.data).get('code','')
        '''sign_del suc'''
        rv = self.sign_del(self.u_id,'222222')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.sign_del(self.ua_id,'222222')
        assert '1' == json.loads(rv.data).get('code','')




    def sign_up(self, name, psw, email):
        return self.app.post('/sign_up', data=dict(
            u_name=name,
            u_psw=psw,
            u_email=email
        ), follow_redirects=True)

    def sign_in(self, loginname, psw):
        return self.app.post('/sign_in',data=dict(
            u_loginname=loginname,
            u_psw=psw
        ),follow_redirects=True)

    def sign_del(self, uid, psw):
        return self.app.post('/safe/sign_del',data=dict(
            u_id=uid,
            u_psw=psw
        ),follow_redirects=True)


    def user_update_info(self, uid, psw, rn, bl, gh, tags, intro):
        return self.app.post('/u/update',data=dict(
            u_id=uid,
            u_psw=psw,
            u_realname=rn,
            u_blog=bl,
            u_github=gh,
            # u_watchusers=waus,
            u_tags=tags,
            u_intro=intro
        ),follow_redirects=True)

    def user_query_info(self, uid):
        return self.app.post('/u/query',data=dict(
            u_id=uid
        ),follow_redirects=True)

    def user_psw_change(self,uid,psw_before,psw):
        return self.app.post('/u/psw/change',data=dict(
            u_id=uid,
            u_psw_before=psw_before,
            u_psw=psw
        ),follow_redirects=True)

    def user_psw_verify(self,loginname,verify):
        return self.app.post('/u/psw/verify',data=dict(
            u_loginname=loginname,
            u_verify=verify
        ),follow_redirects=True)

    def user_psw_reset(self,uid,psw):
        return self.app.post('/u/psw/reset',data=dict(
            u_id=uid,
            u_psw=psw
        ),follow_redirects=True)


    def article_add(self, uid, psw, title, text, tags):
        return self.app.post('/t/add',data=dict(
            u_id=uid,
            u_psw=psw,
            t_title=title,
            t_text=text,
            t_tags=tags,
        ),follow_redirects=True)

    def article_query(self, tid):
        return self.app.post('/t/query',data=dict(
            t_id=tid
        ),follow_redirects=True)

    def article_query_pro(self, tid, uid, psw):
        return self.app.post('/t/query_pro',data=dict(
            t_id=tid,
            u_id=uid,
            u_psw=psw
        ),follow_redirects=True)

    def article_del(self, uid, psw, tid):
        return self.app.post('/t/del',data=dict(
            u_id=uid,
            u_psw=psw,
            t_id=tid
        ),follow_redirects=True)

    def article_update(self, uid, psw, tid, title, text, tags):
        return self.app.post('/t/update',data=dict(
            u_id=uid,
            u_psw=psw,
            t_id=tid,
            t_title=title,
            t_text=text,
            t_tags=tags
        ),follow_redirects=True)

    def article_display(self, tags):
        return self.app.post('/t/display', data=dict(
            t_tags=tags
        ),follow_redirects=True)


    def article_star(self,uid,psw,tid,act):
        return self.app.post('/t/star', data=dict(
            u_id=uid,
            u_psw=psw,
            t_id=tid,
            u_act=act
        ),follow_redirects=True)

    def article_star_unlink(self,uid,psw,tid):
        return self.app.post('/t/star_unlink', data=dict(
            u_id=uid,
            u_psw=psw,
            t_id=tid,
        ),follow_redirects=True)

    def article_recommend(self,uid,psw,tid,act):
        return self.app.post('/t/recommend', data=dict(
            u_id=uid,
            u_psw=psw,
            t_id=tid,
            u_act=act
        ),follow_redirects=True)


    def mail_send(self, uid, email, verify):
        return self.app.post('/u/email/verify', data=dict(
            u_id=uid,
            u_email=email,
            u_verify=verify
        ),follow_redirects=True)

    def mail_pass(self, uid, psw):
        return self.app.post('/u/email/confirm', data=dict(
            u_id=uid,
            u_psw=psw
        ),follow_redirects=True)

    def mail_change(self, uid, psw, email):
        return self.app.post('/u/email/change', data=dict(
            u_id=uid,
            u_psw=psw,
            u_email=email
        ),follow_redirects=True)


    def user_watch(self, uid, psw, uaid, act):
        return self.app.post('/u/follow', data=dict(
            u_id=uid,
            u_psw=psw,
            ua_id=uaid,
            u_act=act
        ),follow_redirects=True)

    def comment_add(self, uid, psw, ectype, ecid, text):
        return self.app.post('/c/add', data=dict(
            u_id=uid,
            u_psw=psw,
            ec_type = ectype,
            ec_id = ecid,
            c_text = text
        ),follow_redirects=True)

    def comment_query(self, cid):
        return self.app.post('/c/query', data=dict(
            c_id = cid,
        ),follow_redirects=True)

    def comment_del(self, uid, psw, cid):
        return self.app.post('/c/del',data=dict(
            u_id=uid,
            u_psw=psw,
            c_id=cid
        ),follow_redirects=True)

    def comment_like(self,uid,psw,cid,act):
        return self.app.post('/c/like', data=dict(
            u_id=uid,
            u_psw=psw,
            c_id=cid,
            u_act=act
        ),follow_redirects=True)

    def reputation_history(self, uid, psw):
        return self.app.post('/u/rep/history',data=dict(
            u_id=uid,
            u_psw=psw,
        ),follow_redirects=True)

    def question_add(self, uid, psw, title, text, tags):
        return self.app.post('/q/add',data=dict(
            u_id=uid,
            u_psw=psw,
            q_title=title,
            q_text=text,
            q_tags=tags
        ),follow_redirects=True)

    def question_query(self, qid):
        return self.app.post('/q/query',data=dict(
            q_id=qid
        ),follow_redirects=True)

    def question_query_pro(self, qid, uid, psw):
        return self.app.post('/q/query_pro',data=dict(
            q_id=qid,
            u_id=uid,
            u_psw=psw
        ),follow_redirects=True)

    def question_del(self, uid, psw, qid):
        return self.app.post('/q/del',data=dict(
            u_id=uid,
            u_psw=psw,
            q_id=qid
        ),follow_redirects=True)

    def question_update(self, uid, psw, qid, title, text, tags):
        return self.app.post('/q/update',data=dict(
            u_id=uid,
            u_psw=psw,
            q_id=qid,
            q_title=title,
            q_text=text,
            q_tags=tags
        ),follow_redirects=True)

    def question_display(self, tags):
        return self.app.post('/q/display', data=dict(
            q_tags=tags
        ),follow_redirects=True)


    def question_star(self,uid,psw,qid,act):
        return self.app.post('/q/star', data=dict(
            u_id=uid,
            u_psw=psw,
            q_id=qid,
            u_act=act
        ),follow_redirects=True)

    def question_star_unlink(self,uid,psw,qid):
        return self.app.post('/q/star_unlink', data=dict(
            u_id=uid,
            u_psw=psw,
            q_id=qid,
        ),follow_redirects=True)

    def question_like(self,uid,psw,qid,act):
        return self.app.post('/q/like', data=dict(
            u_id=uid,
            u_psw=psw,
            q_id=qid,
            u_act=act
        ),follow_redirects=True)


    def answer_add(self, uid, qid, psw, text):
        return self.app.post('/a/add',data=dict(
            u_id=uid,
            q_id=qid,
            u_psw=psw,
            a_text=text,
        ),follow_redirects=True)

    def answer_query(self, aid):
        return self.app.post('/a/query',data=dict(
            a_id=aid
        ),follow_redirects=True)

    def answer_query_pro(self, aid, uid, psw):
        return self.app.post('/a/query_pro',data=dict(
            a_id=aid,
            u_id=uid,
            u_psw=psw
        ),follow_redirects=True)

    def answer_del(self, uid, psw, aid):
        return self.app.post('/a/del',data=dict(
            u_id=uid,
            u_psw=psw,
            a_id=aid
        ),follow_redirects=True)

    def answer_update(self, uid, psw, aid, text):
        return self.app.post('/a/update',data=dict(
            u_id=uid,
            u_psw=psw,
            a_id=aid,
            a_text=text,
        ),follow_redirects=True)

    def answer_star(self,uid,psw,aid,act):
        return self.app.post('/a/star', data=dict(
            u_id=uid,
            u_psw=psw,
            a_id=aid,
            u_act=act
        ),follow_redirects=True)

    def answer_star_unlink(self,uid,psw,aid):
        return self.app.post('/a/star_unlink', data=dict(
            u_id=uid,
            u_psw=psw,
            a_id=aid,
        ),follow_redirects=True)

    def answer_like(self,uid,psw,aid,act):
        return self.app.post('/a/like', data=dict(
            u_id=uid,
            u_psw=psw,
            a_id=aid,
            u_act=act
        ),follow_redirects=True)


    def test_sign_up_fail(self):
        rv = self.app.get('/sign_up?u_name=test.good.name&psw=222222&goodemail@gmail.com', follow_redirects=True)
        assert b'The method is not allowed for the requested URL.' in rv.data
        rv = self.sign_up(self.name,'222222',self.email)
        assert 'username exists' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('te','222222',self.email)
        assert 'username illegal' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('','222222',self.email)
        assert 'username empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('badname','','bad@gmail.com')
        assert 'password empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('badname','22','bad@gmail.com')
        assert 'psw illegal' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('badname','222222','')
        assert 'email empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('badname','222222',self.email)
        assert 'email is existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('badname','222222','badname.gmail.com')
        assert 'email illegal' in json.loads(rv.data).get('codeState','')

    def test_sign_in(self):
        '''fail'''
        rv = self.app.get('/sign_in?u_loginname=test.good.name&psw=222222', follow_redirects=True)
        assert b'The method is not allowed for the requested URL.' in rv.data
        rv = self.sign_in('','222222')
        assert 'login name empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_in(self.name,'')
        assert 'password empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_in('badname','222222')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_in('bad@gmail.com','222222')
        assert 'email not existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_in(self.name,'222223')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')
        '''suc'''
        rv = self.sign_in(self.name,'222222')
        assert '1' == json.loads(rv.data).get('code','')
        assert self.email in json.loads(rv.data).get('u_email','')
        rv = self.sign_in(self.email,'222222')
        assert '1' == json.loads(rv.data).get('code','')
        assert self.name in json.loads(rv.data).get('u_name','')

    def test_sign_del_fail(self):
        rv = self.app.get('/safe/sign_del?u_id=%s&u_psw=222222'%self.u_id, follow_redirects=True)
        assert b'The method is not allowed for the requested URL.' in rv.data
        rv = self.sign_del('','222222')
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_del('100000','222222')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_del(self.u_id,'222223')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')

    def not_test_get_key(self):
        rv = self.app.get('/safe/secret_key', follow_redirects=True)
        assert  b'' in rv.data

    def test_user_psw_change_reset(self):
        rv = self.user_psw_change(self.u_id,'222222','333333')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.sign_in(self.name,'333333')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.user_psw_reset(self.u_id,'222222')
        assert '1' == json.loads(rv.data).get('code','')


    def test_user_update_then_query(self):
        #self, uid, psw, rn, bl, gh, waus, tags
        '''user_update_info'''
        rv = self.user_update_info(self.u_id, '222222', 'Good Name', 'goodblog.com', 'github.com/good', 'node.js', 'I am good~')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.user_update_info(self.u_id, '222223', 'Good Name', 'goodblog.com', 'github.com/good', 'node.js', 'I am good~')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')

        '''user_query_info'''
        rv = self.user_query_info(self.u_id)
        assert 'goodblog.com' in json.loads(rv.data).get('u_blog','')
        rv = self.user_query_info('')
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.user_query_info('100000')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')

    def test_user_watch(self):
        '''watch and unwatch, suc and fail'''
        rv = self.user_watch(self.u_id, '222222', self.ua_id, '1')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.sign_in(self.name,'222222')
        assert self.ua_id in json.loads(rv.data).get('u_watchusers','')
        rv = self.sign_in(self.name2,'222222')
        assert self.u_id in json.loads(rv.data).get('u_watchusers','')
        rv = self.user_watch(self.u_id, '222222', self.ua_id, '1')
        assert 'user already watched' in json.loads(rv.data).get('codeState','')

        rv = self.user_watch(self.u_id, '222222', self.ua_id, '0')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.sign_in(self.name,'222222')
        assert self.ua_id not in json.loads(rv.data).get('u_watchusers','')
        rv = self.sign_in(self.name2,'222222')
        assert self.u_id not in json.loads(rv.data).get('u_watchusers','')
        rv = self.user_watch(self.u_id, '222222', self.ua_id, '0')
        assert 'user already unwatched' in json.loads(rv.data).get('codeState','')


    def test_mail_send(self):
        '''send verified email, this test is annoying. once enough, i think..'''
        rv = self.app.get('/public/get_verify', follow_redirects=True)
        verify_code = rv.data
        assert len(verify_code)==5
        '''email_confirm'''
        rv = self.mail_send(self.ua_id, '1401520070@qq.com', verify_code)
        assert '1' == json.loads(rv.data).get('code','')
        '''psw_change'''
        rv = self.user_psw_verify(self.name2, verify_code)
        assert '1' == json.loads(rv.data).get('code','')


    def test_mail_confirm_change(self):
        '''confirm user email'''
        rv = self.mail_pass(self.ua_id,'222222')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.sign_in(self.name2,'222222')
        assert 1 == json.loads(rv.data).get('u_email_confirm','')
        '''change email'''
        rv = self.mail_change(self.ua_id,'222222','anotheremail@gmail.com')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.sign_in('anotheremail@gmail.com','222222')
        assert 0 == json.loads(rv.data).get('u_email_confirm','')
        '''fail'''
        rv = self.mail_pass('','222222')
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.mail_pass('100000','222222')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.mail_pass(self.ua_id,'222223')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')


    def test_mail_change_fail(self):
        rv = self.mail_change('','222222','anotheremail@gmail.com')
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.mail_change('100000','222222','anotheremail@gmail.com')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.mail_change(self.ua_id,'','anotheremail@gmail.com')
        assert 'password empty' in json.loads(rv.data).get('codeState','')
        rv = self.mail_change(self.ua_id,'222223','anotheremail@gmail.com')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')
        rv = self.sign_in('anotheremail@gmail.com','222222')
        assert 'email not existed' in json.loads(rv.data).get('codeState','')


    def test_article_add_fail(self):
        '''add_fail'''
        rv = self.article_add('', '222222', 'Title', 'Text', 'node.js')
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.article_add('100000', '222222', 'title', 'text', 'node.js')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.article_add(self.u_id, '', 'Title', 'Text', 'node.js')
        assert 'password empty' in json.loads(rv.data).get('codeState','')
        rv = self.article_add(self.u_id, '222221', 'Title', 'Text', 'node.js')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')
        rv = self.article_add(self.u_id, '222222', '', 'Text', 'node.js')
        assert 'article title empty' in json.loads(rv.data).get('codeState','')
        rv = self.article_add(self.u_id, '222222', 'Title', '', 'node.js')
        assert 'article text empty' in json.loads(rv.data).get('codeState','')
        '''query_fail, suc_test is everywhere'''
        rv = self.article_query('')
        assert 'article id empty' in json.loads(rv.data).get('codeState','')
        rv = self.article_query('100000')
        assert 'article not existed' in json.loads(rv.data).get('codeState','')


    def test_article_del_fail(self):
        '''delete_fail'''
        rv = self.article_del('', '222222', self.t_id)
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.article_del('100000', '222222', self.t_id)
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.article_del(self.u_id, '', self.t_id)
        assert 'password empty' in json.loads(rv.data).get('codeState','')
        rv = self.article_del(self.u_id, '222223', self.t_id)
        assert 'wrong password' in json.loads(rv.data).get('codeState','')
        rv = self.article_del(self.u_id, '222222', '')
        assert 'article id empty' in json.loads(rv.data).get('codeState','')
        rv = self.article_del(self.u_id, '222222', '100000')
        assert 'article not existed' in json.loads(rv.data).get('codeState','')
        rv = self.article_del(self.ua_id, '222222', self.t_id)
        assert 'no access to modify article' in json.loads(rv.data).get('codeState','')


    def test_article_display(self):
        rv = self.article_add(self.ua_id, '222222', 'Python Version',
'''To support multiple versions, the programs named python and pythonw select the real ver-
sion of Python to run, depending on various settings.  The current supported versions are
2.6 and 2.7, with the default being 2.7.  Use

   % man python2.6
   % man python2.7
   % man pythonw2.6
   % man pythonw2.7

to see the man page for a specific version.  Without a version specified these will show
the man page for the (unmodified) default version of Python (2.7).  To see the man page
for a specific version of pydoc, for example, use
''', 'python')
        self.ta_id = json.loads(rv.data).get('t_id','')
        rv = self.article_display('node.js,python')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.article_display('')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.article_del(self.ua_id, '222222', self.ta_id)
        assert '1' == json.loads(rv.data).get('code','')

    def test_article_update(self):
        '''check if text changed'''
        text = gene_id(num=20,letter=True)
        rv = self.article_update(self.u_id, '222222', self.t_id, 'What\'s nodejs', text, 'nodejs')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.article_query(self.t_id)
        assert text in json.loads(rv.data).get('t_text','')

    def test_comment_add_del_query_suc(self):
        rv = self.comment_add(self.ua_id, '222222', 'article', self.t_id, 'js is shit!')
        assert '1' == json.loads(rv.data).get('code','')
        self.c_id = json.loads(rv.data).get('c_id','')
        '''like'''
        rv = self.comment_like(self.u_id,'222222',self.c_id,'0')
        assert 'nothing happended' == json.loads(rv.data).get('message','')
        rv = self.comment_like(self.u_id,'222222',self.c_id,'1')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.comment_like(self.u_id,'222222',self.c_id,'1')
        assert 'comment like already' == json.loads(rv.data).get('codeState','')
        rv = self.comment_like(self.u_id,'222222',self.c_id,'0')
        assert 'like cancel' == json.loads(rv.data).get('message','')
        rv = self.comment_like(self.u_id,'222222',self.c_id,'-1')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.comment_like(self.u_id,'222222',self.c_id,'-1')
        assert 'comment dislike already' == json.loads(rv.data).get('codeState','')
        rv = self.comment_like(self.u_id,'222222',self.c_id,'0')
        assert 'dislike cancel' == json.loads(rv.data).get('message','')

        rv = self.comment_query(self.c_id)
        assert json.loads(rv.data).get('c_id','') == int(self.c_id)
        rv = self.article_query(self.t_id)
        assert self.c_id in json.loads(rv.data).get('t_comments','')
        rv = self.comment_del(self.ua_id, '222222', self.c_id)
        assert '1' == json.loads(rv.data).get('code','')



    def test_article_starlike_and_querypro(self):
        '''rep test'''
        rv = self.reputation_history(self.u_id,'222222')
        assert bool(json.loads(rv.data).get('history',''))

        rv = self.article_recommend(self.ua_id, '222222', self.t_id, '0')
        assert 'article not recommend' in json.loads(rv.data).get('codeState','')
        rv = self.article_recommend(self.ua_id, '222222', self.t_id, '1')
        assert '1' == json.loads(rv.data).get('code','')
        '''query_pro test'''
        rv = self.article_query_pro(self.t_id, self.ua_id, '222222')
        assert '0' == json.loads(rv.data).get('t_star_bool','')
        assert '1' == json.loads(rv.data).get('t_recommend_bool','')
        '''rep test'''
        rv = self.reputation_history(self.u_id,'222222')
        assert len(json.loads(rv.data).get('history','')) == 2
        '''test end'''
        rv = self.article_recommend(self.ua_id, '222222', self.t_id, '0')
        assert '1' == json.loads(rv.data).get('code','')

        rv = self.article_star(self.ua_id, '222222', self.t_id, '0')
        assert 'article not star' in json.loads(rv.data).get('codeState','')
        rv = self.article_star(self.ua_id, '222222', self.t_id, '1')
        assert '1' == json.loads(rv.data).get('code','')
        '''query_pro test'''
        rv = self.article_query_pro(self.t_id, self.ua_id, '222222')
        assert '1' == json.loads(rv.data).get('t_star_bool','')
        assert '0' == json.loads(rv.data).get('t_recommend_bool','')
        '''test end'''
        rv = self.article_star(self.ua_id, '222222', self.t_id, '0')
        assert '1' == json.loads(rv.data).get('code','')


    def test_question(self):
        '''add'''
        rv = self.question_add(self.u_id, '222222', 'who am i', 'RT', '')
        assert '1' == json.loads(rv.data).get('code','')
        self.q_id = json.loads(rv.data).get('q_id','')
        '''update'''
        rv = self.question_update(self.u_id, '222222', self.q_id, 'Who am I?', 'RT', 'node.js')
        assert '1' == json.loads(rv.data).get('code','')
        '''star'''
        rv = self.question_query_pro(self.q_id, self.u_id, '222222')
        assert '0' == json.loads(rv.data).get('q_star_bool','')
        rv = self.question_star(self.u_id,'222222',self.q_id,'1')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.question_query_pro(self.q_id, self.u_id, '222222')
        assert '1' == json.loads(rv.data).get('q_star_bool','')
        rv = self.question_star(self.u_id,'222222',self.q_id,'1')
        assert 'question star already' == json.loads(rv.data).get('codeState','')
        rv = self.question_star(self.u_id,'222222',self.q_id,'0')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.question_query_pro(self.q_id, self.u_id, '222222')
        assert '0' == json.loads(rv.data).get('q_star_bool','')
        rv = self.question_star(self.u_id,'222222',self.q_id,'0')
        assert 'question not star' == json.loads(rv.data).get('codeState','')
        '''like'''
        rv = self.question_like(self.u_id,'222222',self.q_id,'0')
        assert 'nothing happended' == json.loads(rv.data).get('message','')
        rv = self.question_like(self.u_id,'222222',self.q_id,'1')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.question_like(self.u_id,'222222',self.q_id,'1')
        assert 'question like already' == json.loads(rv.data).get('codeState','')
        rv = self.question_like(self.u_id,'222222',self.q_id,'0')
        assert 'like cancel' == json.loads(rv.data).get('message','')
        rv = self.question_like(self.u_id,'222222',self.q_id,'-1')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.question_like(self.u_id,'222222',self.q_id,'-1')
        assert 'question dislike already' == json.loads(rv.data).get('codeState','')
        rv = self.question_like(self.u_id,'222222',self.q_id,'0')
        assert 'dislike cancel' == json.loads(rv.data).get('message','')
        '''query'''
        rv = self.question_query(self.q_id)
        assert '1' == json.loads(rv.data).get('code','')
        '''display'''
        rv = self.question_display('node.js,python')
        assert '1' == json.loads(rv.data).get('code','')
        '''del'''
        rv = self.question_del(self.ua_id, '222222', self.q_id)
        assert 'no access to modify question' in json.loads(rv.data).get('codeState','')
        rv = self.question_del(self.u_id, '222222', self.q_id)
        assert '1' == json.loads(rv.data).get('code','')




    def test_answer(self):
        '''setUp: question_add'''
        rv = self.question_add(self.u_id, '222222', 'Who am I?', 'RT', '')
        assert '1' == json.loads(rv.data).get('code','')
        self.q_id = json.loads(rv.data).get('q_id','')

        '''add'''
        rv = self.answer_add(self.ua_id, self.q_id, '222222', 'You are %s'%self.name)
        assert '1' == json.loads(rv.data).get('code','')
        self.a_id = json.loads(rv.data).get('a_id','')
        '''update'''
        rv = self.answer_update(self.u_id, '222222', self.a_id, 'I don\'t know...')
        assert 'no access to modify answer' in json.loads(rv.data).get('codeState','')
        rv = self.answer_update(self.ua_id, '222222', self.a_id, 'I don\'t know...')
        assert '1' == json.loads(rv.data).get('code','')
        '''star'''
        rv = self.answer_query_pro(self.a_id, self.u_id, '222222')
        assert '0' == json.loads(rv.data).get('a_star_bool','')
        rv = self.answer_star(self.u_id,'222222',self.a_id,'1')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.answer_query_pro(self.a_id, self.u_id, '222222')
        assert '1' == json.loads(rv.data).get('a_star_bool','')
        rv = self.answer_star(self.u_id,'222222',self.a_id,'1')
        assert 'answer star already' == json.loads(rv.data).get('codeState','')
        rv = self.answer_star(self.u_id,'222222',self.a_id,'0')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.answer_query_pro(self.a_id, self.u_id, '222222')
        assert '0' == json.loads(rv.data).get('a_star_bool','')
        rv = self.answer_star(self.u_id,'222222',self.a_id,'0')
        assert 'answer not star' == json.loads(rv.data).get('codeState','')
        '''like'''
        rv = self.answer_like(self.u_id,'222222',self.a_id,'0')
        assert 'nothing happended' == json.loads(rv.data).get('message','')
        rv = self.answer_like(self.u_id,'222222',self.a_id,'1')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.answer_like(self.u_id,'222222',self.a_id,'1')
        assert 'answer like already' == json.loads(rv.data).get('codeState','')
        rv = self.answer_like(self.u_id,'222222',self.a_id,'0')
        assert 'like cancel' == json.loads(rv.data).get('message','')
        rv = self.answer_like(self.u_id,'222222',self.a_id,'-1')
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.answer_like(self.u_id,'222222',self.a_id,'-1')
        assert 'answer dislike already' == json.loads(rv.data).get('codeState','')
        rv = self.answer_like(self.u_id,'222222',self.a_id,'0')
        assert 'dislike cancel' == json.loads(rv.data).get('message','')

        '''delete'''
        rv = self.answer_del(self.u_id, '222222', self.a_id)
        assert '1' == json.loads(rv.data).get('code','')
        rv = self.answer_del(self.ua_id, '222222', self.a_id)
        assert 'answer not existed' in json.loads(rv.data).get('codeState','')
        '''tearDown: question_del'''
        rv = self.question_del(self.u_id, '222222', self.q_id)
        assert '1' == json.loads(rv.data).get('code','')


if __name__ == '__main__':
    unittest.main()
