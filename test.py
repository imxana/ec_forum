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
        rv = self.sign_up('test.another.name','222222','anotheremail@gmail.com')
        self.ua_id = json.loads(rv.data).get('u_id','')
        assert '1' in json.loads(rv.data).get('code','')

    def tearDown(self):
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
        return self.app.post('/sign_del',data=dict(
            u_id=uid,
            u_psw=psw
        ),follow_redirects=True)

    def user_update_info(self, uid, psw, rn, bl, gh, waus, tags):
        return self.app.post('/u/update',data=dict(
            u_id=uid,u_psw=psw,
            u_realname=rn,
            u_blog=bl,
            u_github=gh,
            u_watchusers=waus,
            u_tags=tags
        ),follow_redirects=True)

    def user_query_info(self, uid):
        return self.app.post('/u/query',data=dict(
            u_id=uid
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
        # print('test:92',json.loads(rv.data))
        assert '1' in json.loads(rv.data).get('code','')
        assert 'goodemail@gmail.com' in json.loads(rv.data).get('u_email','')
        rv = self.sign_in('goodemail@gmail.com','222222')
        assert '1' in json.loads(rv.data).get('code','')
        assert 'test.good.name' in json.loads(rv.data).get('u_name','')



    def test_sign_del_fail(self):
        rv = self.app.get('/sign_del?u_id=%s&u_psw=222222'%self.u_id, follow_redirects=True)
        assert b'The method is not allowed for the requested URL.' in rv.data
        rv = self.sign_del('','222222')
        assert 'userid empty' in json.loads(rv.data).get('codeState','')
        rv = self.sign_del('000000','222222')
        assert 'user not existed' in json.loads(rv.data).get('codeState','')
        rv = self.sign_del(self.u_id,'222223')
        assert 'wrong password' in json.loads(rv.data).get('codeState','')


    def test_user_update_query(self):
        #self, uid, psw, rn, bl, gh, waus, tags
        rv = self.user_update_info(self.u_id, '222222', 'Good Name', 'goodblog.com', 'github.com/good', self.ua_id, 'node.js')
        assert '1' in json.loads(rv.data).get('code','')
        rv = self.user_query_info(self.u_id)
        # print(118, rv.data)
        assert 'goodblog.com' in json.loads(rv.data).get('u_blog','')




if __name__ == '__main__':
    unittest.main()
