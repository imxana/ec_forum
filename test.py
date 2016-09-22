from flask import json
import unittest
import tempfile
import app as ec

class ECTestCase(unittest.TestCase):
    
    def setUp(self):
        #ec.config['TESTING'] = True
        self.app = ec.app.test_client()

    def tearDown(self):
        pass

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
    
    def test_up_in_del(self):
        '''sign_up suc'''
        rv = self.sign_up('xana','222222','xana.awaken@gmail.com')
        assert b'u_id' in rv.data
        u_id = json.loads(rv.data).get('u_id','')

        '''sign_up fail'''
        rv = self.sign_up('xana','222222','xana.awaken@gmail.com')
        assert b'username is existed' in rv.data
        rv = self.sign_up('xa','222222','xana.awaken@gmail.com')
        assert b'username illegal' in rv.data
        rv = self.sign_up('','222222','xana.awaken@gmail.com')
        assert b'username empty' in rv.data
        rv = self.sign_up('hana','','hana@gmail.com')
        assert b'password empty' in rv.data
        rv = self.sign_up('hana','22','hana@gmail.com')
        assert b'psw illegal' in rv.data
        rv = self.sign_up('hana','222222','')
        assert b'email empty' in rv.data
        rv = self.sign_up('hana','222222','xana.awaken@gmail.com')
        assert b'email is existed' in rv.data
        rv = self.sign_up('hana','222222','hana.gmail.com')
        assert b'email illegal' in rv.data


        '''sign_in suc'''        
        rv = self.sign_in('xana','222222')
        assert b'u_email_confirm' in rv.data
        rv = self.sign_in('xana.awaken@gmail.com','222222')
        assert b'u_email_confirm' in rv.data


        '''sign_in fail'''
        rv = self.sign_in('','222222')
        assert b'login name empty' in rv.data
        rv = self.sign_in('xana','')
        assert b'password empty' in rv.data
        rv = self.sign_in('hana','222222')
        assert b'user not existed' in rv.data
        rv = self.sign_in('hana@gmail.com','222222')
        assert b'email not existed' in rv.data
        rv = self.sign_in('xana','222223')
        assert b'wrong password' in rv.data

        
        '''sign_del fail'''
        rv = self.sign_del('','222222')
        assert b'userid empty' in rv.data
        rv = self.sign_del('000000','222222')
        assert b'user not existed' in rv.data
        rv = self.sign_del(u_id,'222223')
        assert b'wrong password' in rv.data

        '''sign_del suc'''
        rv = self.sign_del(u_id,'222222')
        assert b'u_id' in rv.data

        

if __name__ == '__main__':
    unittest.main()



