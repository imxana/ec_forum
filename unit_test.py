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
        return self.app.post('/sign_up', data=dict(u_name=name,u_psw=psw,u_email=email), follow_redirects=True)
    def sign_del(self, uid, psw):
        return self.app.post('/safe/sign_del',data=dict(u_id=uid,u_psw=psw),follow_redirects=True)
    def article_add(self, uid, psw, title, text, tags):
        return self.app.post('/t/add',data=dict(u_id=uid,u_psw=psw,t_title=title,t_text=text,t_tags=tags,),follow_redirects=True)
    def article_del(self, uid, psw, tid):
        return self.app.post('/t/del',data=dict(u_id=uid,u_psw=psw,t_id=tid),follow_redirects=True)
    def article_query(self, tid):
        return self.app.post('/t/query',data=dict(t_id=tid),follow_redirects=True)
    def article_display(self, tags):
        return self.app.post('/t/display', data=dict(t_tags=tags),follow_redirects=True)

    def test_test(self):
        rv = self.article_display('node.js')
        print('ut 76:', rv.data)
        rv = self.article_query(self.t_id)
        print('ut 78:', rv.data)

if __name__ == '__main__':
    unittest.main()
