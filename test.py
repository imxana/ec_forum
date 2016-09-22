from flask import json
import unittest
import tempfile
import app as ec

class ECTestCase(unittest.TestCase):

    u_id = ''
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
        '''sign_up'''
        rv = self.sign_up('xana','222222','xana.awaken@gmail.com')
        print(38, rv.data)
        assert b'u_id' in rv.data
        u_id = json.loads(rv.data).get('u_id','')
        print(41,u_id)
        rv = self.sign_up('xana','222222','xana.awaken@gmail.com')
        assert b'username is existed' in rv.data

        '''sign_in'''        
        rv = self.sign_in('xana','222222')
        assert b'u_email_confirm' in rv.data
        rv = self.sign_in('xana','222222')
        assert b'u_email_confirm' in rv.data

        '''sign_del'''
        rv = self.sign_del(u_id,'222222')
        print(53, rv.data)
        assert b'u_id' in rv.data

        

if __name__ == '__main__':
    unittest.main()



