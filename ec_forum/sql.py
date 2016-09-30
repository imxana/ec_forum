# coding:utf8
import pymysql
from ec_forum.id_dealer import gene_id

conn = pymysql.Connect(
    host = '127.0.0.1',
    user = 'root',
    passwd = '',
    db = 'ec_forum',
    charset = 'utf8'
)

class sqlQ(object):

    def signup_insert(self,name,email,psw):
        '''insert without check'''
        err,u_id = True,gene_id()
        cursor = conn.cursor()
        while self.userid_search(u_id, table='ec_user'):
            u_id = gene_id()
        # u_realname text comment '真实姓名',
        # u_blog text comment '博客地址',
        # u_github text comment 'github地址',
        # u_articles text comment '文章ID组，我的和收藏',
        # u_questions text comment '提问ID组，我的和关注',
        # u_answers text comment '回答ID组，我的和关注',
        # u_watchusers text comment '关注用户ID组',
        # u_tags text comment '关注标签',
        # u_intro text comment '个人签名'
        sql = "insert into ec_user(u_name, u_email, u_psw, u_id, u_email_confirm, u_level, u_reputation, u_articles,u_questions,u_answers,u_watchusers) \
            values('%s','%s','%s',%s,0,2,0,'&','&','&','&');" % (name,email,psw,u_id)
        try:
            if cursor.execute(sql) == 1:
                if cursor.rowcount == 1:
                    conn.commit()
                    err = False
        except Exception as e:
            raise Exception('sign_up failed')
            conn.rollback()
        finally:
            cursor.close()
        return err, u_id


    def signup_select(self, name, method='u_name'):
        '''check if some property exist'''
        cursor = conn.cursor()
        exist = True
        sql = "select * from ec_user where %s='%s';" % (method, name)
        try:
            cursor.execute(sql)
            rs = cursor.fetchone()
            # if not bool(rs):
            #    exist = False
            exist = bool(rs)
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return exist


    def signin_select(self, loginname, method='u_name'):
        '''sign in by name or email to get the tuple'''
        cursor = conn.cursor()
        err,res = True,()
        sql = "select * from ec_user where %s='%s';" % (method,loginname)
        try:
            if cursor.execute(sql) == 1:
                rs = cursor.fetchone()
                if bool(rs):
                    err,res = False,rs
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return err,res


    def sign_del(self, uid):
        '''delelte account, just for test!!!'''
        cursor = conn.cursor()
        err = True
        sql = "delete from ec_user where u_id='%s';" % uid
        try:
            st = cursor.execute(sql)
            if st == 1:
                err = False
                conn.commit()
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return err


    def userid_search(self, ec_id, table='ec_user'):
        '''search existense of an id'''
        cursor = conn.cursor()
        exist = True
        query_name = 'u_id'
        if table == 'ec_article':
            query_name = 't_id'
        elif table == 'ec_question':
            query_name = 'q_id'
        elif table == 'ec_comment':
            query_name = 'c_id'
        elif table == 'ec_answer':
            query_name = 'a_id'
        sql = "select * from %s where %s='%s';" % (table,query_name,ec_id)
        try:
            cursor.execute(sql)
            rs = cursor.fetchone()
            exist = bool(rs)
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return exist


    def user_update(self, u_id, info):
        '''update the infomation'''
        cursor = conn.cursor()
        err = True
        if len(info) == 0:
            return err
        sql = "update ec_user set "
        for k,v in info.items():
            sql += "%s='%s',"%(k,v)
        sql = sql[:-1] + " where u_id='%s'"%u_id
        # print('sql.py 118',sql)
        try:
            if cursor.execute(sql) == 1:
                err = False
                conn.commit()
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return err


    def article_insert(self, u_id, u_psw, t_title, t_text, t_tags):
        '''insert an article without check'''
        cursor = conn.cursor()
        err,t_id = True,gene_id()
        while self.userid_search(t_id, table='ec_article'):
            t_id = gene_id()
        sql = "insert into ec_article(t_id, u_id, t_title, t_text, t_date, t_like, t_comments, t_tags, t_date_latest) values(%s,%s,'%s','%s',curdate(),0,'','%s', curdate());"%(t_id, u_id, t_title, t_text, t_tags)
        try:
            if cursor.execute(sql) == 1:
                if cursor.rowcount == 1:
                    conn.commit()
                    err = False
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return err,t_id


    def article_select(self, t_id):
        '''select article just by t_id'''
        cursor = conn.cursor()
        err,res = True,()
        sql = "select * from ec_article where t_id='%s';" % t_id
        try:
            if cursor.execute(sql) == 1:
                rs = cursor.fetchone()
                if bool(rs):
                    err,res = False,rs
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return err,res


    def article_del(self, tid):
        '''easy article delete'''
        cursor = conn.cursor()
        err = True
        sql = "delete from ec_article where t_id='%s';" % tid
        try:
            st = cursor.execute(sql)
            if st == 1:
                err = False
                conn.commit()
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return err
