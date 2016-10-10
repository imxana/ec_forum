from flask import json
import unittest
import tempfile
import app as ec

class ECTestCase(unittest.TestCase):

    def setUp(self):
        #ec.config['TESTING'] = True
        self.app = ec.app.test_client()
        '''sign_up suc'''
        rv = self.sign_up('test.good.name','222222','goodemail@gmail.com')
        self.u_id = json.loads(rv.data).get('u_id','')
        assert '1' in json.loads(rv.data).get('code','')
        rv = self.sign_up('test.another.name','222222','1401520070@qq.com')
        self.ua_id = json.loads(rv.data).get('u_id','')
        assert '1' in json.loads(rv.data).get('code','')

        '''add_suc'''
        rv = self.article_add(self.u_id, '222222', 'Title', 'Text', 'node.js')
        self.t_id = json.loads(rv.data).get('t_id','')
        assert '1' in json.loads(rv.data).get('code','')

    def tearDown(self):
        '''article_del_suc'''
        rv = self.article_del(self.u_id, '222222', self.t_id)
        assert '1' in json.loads(rv.data).get('code','')

        '''sign_del suc'''
        rv = self.sign_del(self.u_id,'222222')
        assert '1' in json.loads(rv.data).get('code','')
        rv = self.sign_del(self.ua_id,'222222')
        assert '1' in json.loads(rv.data).get('code','')




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

    def article_del(self, uid, psw, tid):
        return self.app.post('/t/del',data=dict(
            u_id=uid,
            u_psw=psw,
            t_id=tid
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
        return self.app.post('/u/watchuser', data=dict(
            u_id=uid,
            u_psw=psw,
            ua_id=uaid,
            u_act=act
        ),follow_redirects=True)


    def test_sign_up_fail(self):
        rv = self.app.get('/sign_up?u_name=test.good.name&psw=222222&goodemail@gmail.com', follow_redirects=True)
        assert b'The method is not allowed for the requested URL.' in rv.data
        rv = self.sign_up('test.good.name','222222','goodemail@gmail.com')
        assert 'username is existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('te','222222','goodemail@gmail.com')
        assert 'username illegal' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('','222222','goodemail@gmail.com')
        assert 'username empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('test.bad.name','','bad@gmail.com')
        assert 'password empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('test.bad.name','22','bad@gmail.com')
        assert 'psw illegal' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('test.bad.name','222222','')
        assert 'email empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('test.bad.name','222222','goodemail@gmail.com')
        assert 'email is existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_up('test.bad.name','222222','test.bad.name.gmail.com')
        assert 'email illegal' in json.loads(rv.data).get('codeState','')

    def test_sign_in_failed(self):
        rv = self.app.get('/sign_in?u_loginname=test.good.name&psw=222222', follow_redirects=True)
        assert b'The method is not allowed for the requested URL.' in rv.data
        rv = self.sign_in('','222222')
        assert 'login name empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_in('test.good.name','')
        assert 'password empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_in('test.bad.name','222222')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_in('bad@gmail.com','222222')
        assert 'email not existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_in('test.good.name','222223')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')

    def test_sign_in_suc(self):
        rv = self.sign_in('test.good.name','222222')
        assert '1' in json.loads(rv.data).get('code','')
        assert 'goodemail@gmail.com' in json.loads(rv.data).get('u_email','')
        rv = self.sign_in('goodemail@gmail.com','222222')
        assert '1' in json.loads(rv.data).get('code','')
        assert 'test.good.name' in json.loads(rv.data).get('u_name','')

    def test_sign_del_fail(self):
        rv = self.app.get('/safe/sign_del?u_id=%s&u_psw=222222'%self.u_id, follow_redirects=True)
        assert b'The method is not allowed for the requested URL.' in rv.data
        rv = self.sign_del('','222222')
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_del('100000','222222')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_del(self.u_id,'222223')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')

    def test_get_key(self):
        rv = self.app.get('/safe/secret_key', follow_redirects=True)
        assert '1' in json.loads(rv.data).get('code','')

    def test_user_update_then_query(self):
        #self, uid, psw, rn, bl, gh, waus, tags
        '''user_update_info'''
        rv = self.user_update_info(self.u_id, '222222', 'Good Name', 'goodblog.com', 'github.com/good', 'node.js', 'I am good~')
        assert '1' in json.loads(rv.data).get('code','')
        rv = self.user_update_info(self.u_id, '222223', 'Good Name', 'goodblog.com', 'github.com/good', 'node.js', 'I am good~')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')

        '''user_query_info'''
        rv = self.user_query_info(self.u_id)
        assert 'goodblog.com' in json.loads(rv.data).get('u_blog','')
        rv = self.user_query_info('')
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.user_query_info('100000')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')

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

    def test_article_query_suc(self):
        '''query_suc'''
        rv = self.article_query(self.t_id)
        assert '1' in json.loads(rv.data).get('code','')

    def test_article_query_fail(self):
        '''query_fail'''
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
        assert 'have no access to do it' in json.loads(rv.data).get('codeState','')

    def ntest_mail_send(self):
        '''send verified email, this test is annoying. once enough, i think'''
        rv = self.app.get('/public/get_verify', follow_redirects=True)
        verify_code = rv.data
        assert len(verify_code)==5
        rv = self.mail_send(self.ua_id, '1401520070@qq.com', verify_code)
        assert '1' in json.loads(rv.data).get('code','')

    def test_mail_confirm_suc(self):
        '''confirm user email'''
        rv = self.mail_pass(self.ua_id,'222222')
        assert '1' in json.loads(rv.data).get('code','')
        rv = self.sign_in('test.another.name','222222')
        assert 1 == json.loads(rv.data).get('u_email_confirm','')

    def test_mail_confirm_fail(self):
        rv = self.mail_pass('','222222')
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.mail_pass('100000','222222')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.mail_pass(self.ua_id,'222223')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')

    def test_mail_change_suc(self):
        '''change email'''
        rv = self.mail_change(self.ua_id,'222222','anotheremail@gmail.com')
        assert '1' in json.loads(rv.data).get('code','')
        rv = self.sign_in('anotheremail@gmail.com','222222')
        assert 0 == json.loads(rv.data).get('u_email_confirm','')

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

    def test_watch_user(self):
        '''watch and unwatch, suc and fail'''
        rv = self.user_watch(self.u_id, '222222', self.ua_id, '1')
        assert '1' in json.loads(rv.data).get('code','')
        rv = self.sign_in('test.good.name','222222')
        assert self.ua_id in json.loads(rv.data).get('u_watchusers','')
        rv = self.sign_in('test.another.name','222222')
        assert self.u_id in json.loads(rv.data).get('u_watchusers','')
        rv = self.user_watch(self.u_id, '222222', self.ua_id, '1')
        assert 'user already watched' in json.loads(rv.data).get('codeState','')

        rv = self.user_watch(self.u_id, '222222', self.ua_id, '0')
        assert '1' in json.loads(rv.data).get('code','')
        rv = self.sign_in('test.good.name','222222')
        assert self.ua_id not in json.loads(rv.data).get('u_watchusers','')
        rv = self.sign_in('test.another.name','222222')
        assert self.u_id not in json.loads(rv.data).get('u_watchusers','')
        rv = self.user_watch(self.u_id, '222222', self.ua_id, '0')
        assert 'user already unwatched' in json.loads(rv.data).get('codeState','')



if __name__ == '__main__':
    unittest.main()

