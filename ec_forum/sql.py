# coding:utf8
import pymysql, threading
from ec_forum.id_dealer import gene_id


def get_conn():
    return pymysql.Connect(host='127.0.0.1',user='root',passwd='',db='ec_forum',charset='utf8')
# conn = get_conn()


'''pymysql socket pool'''
socket_limit = 10
socket_auto_update = False
socket_pool = []
socket_update = socket_limit

for i in range(socket_limit):
    socket_pool.append(get_conn())

def update_conn():
    global socket_update
    socket_update+=1
    if socket_update >= socket_limit:
        socket_update = 0
    print("[update pymysql connection..]")
    socket_pool[socket_update] = get_conn()
    global t    #Notice: use global variable!
    t = threading.Timer(7200.0, update_conn)
    t.start()

t = threading.Timer(7200.0, update_conn)
if socket_auto_update:
    t.start()


class sqlQ(object):

    def signup_insert(self,name,email,psw):
        '''insert without check'''
        conn = socket_pool.pop()
        err,u_id = True,gene_id()
        cursor = conn.cursor()
        while self.userid_search(u_id, table='ec_user'):
            u_id = gene_id()
        sql = "insert into ec_user(u_name, u_email, u_psw, u_id, u_email_confirm, u_level, u_reputation, u_articles, u_questions,u_answers,u_watchusers) \
values(%r,%r,%r,%s,0,2,0,'&','&','&','&');" % (name,email,psw,u_id)
        try:
            if cursor.execute(sql) == 1:
                if cursor.rowcount == 1:
                    conn.commit()
                    err = False
        except Exception as e:
            print(e)
            conn = get_conn()
            conn.rollback()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err, u_id


    def signup_select(self, name, method='u_name'):
        '''check if some property exist'''

        conn = socket_pool.pop()
        cursor = conn.cursor()
        exist = True
        sql = "select * from ec_user where %s=%r;" % (method, name)
        try:
            cursor.execute(sql)
            rs = cursor.fetchone()
            exist = bool(rs)
        except Exception as e:
            print(e)
            conn = get_conn()
            conn.rollback()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return exist


    def signin_select(self, loginname, method='u_name'):
        '''sign in by name or email to get the tuple'''

        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,res = True,()
        sql = "select * from ec_user where %s=%r;" % (method,loginname)
        try:
            if cursor.execute(sql) == 1:
                rs = cursor.fetchone()
                if bool(rs):
                    err,res = False,rs
        except Exception as e:
            print(e)
            conn.rollback()
            conn = get_conn()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err,res


    def sign_del(self, uid):
        '''delelte account, just for test!!!'''

        conn = socket_pool.pop()
        cursor = conn.cursor()
        err = True
        sql = "delete from ec_user where u_id=%r;" % uid
        try:
            st = cursor.execute(sql)
            if st == 1:
                err = False
                conn.commit()
        except Exception as e:
            print(e)
            conn = get_conn()
            conn.rollback()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err


    def userid_search(self, ec_id, table='ec_user'):
        '''search existense of an id'''

        conn = socket_pool.pop()
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
        sql = "select * from %s where %s=%r;" % (table,query_name,ec_id)
        try:
            cursor.execute(sql)
            rs = cursor.fetchone()
            exist = bool(rs)
        except Exception as e:
            print(e)
            conn = get_conn()
            conn.rollback()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return exist


    def user_update(self, u_id, info):
        '''update the infomation'''

        conn = socket_pool.pop()
        cursor = conn.cursor()
        err = True
        if len(info) == 0:
            return err
        sql = "update ec_user set "
        for k,v in info.items():
            sql += "%s=%r,"%(k,v)
        sql = sql[:-1] + " where u_id=%r;"%u_id
        try:
            if cursor.execute(sql) == 1:
                err = False
                conn.commit()
        except Exception as e:
            print(e)
            conn = get_conn()
            conn.rollback()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err


    def article_insert(self, u_id, u_psw, t_title, t_text, t_tags):
        '''insert an article without check'''

        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,t_id = True,gene_id()
        while self.userid_search(t_id, table='ec_article'):
            t_id = gene_id()
        sql = "insert into ec_article(t_id, u_id, t_title, t_text, t_date, t_like, t_comments, t_tags, t_date_latest, t_star) values(%s,%s,%r,%r,curtime(),0,'',%r, curtime(),0);"%(t_id, u_id, t_title, t_text, t_tags)
        # print('sql.py 145',sql)
        try:
            if cursor.execute(sql) == 1:
                if cursor.rowcount == 1:
                    conn.commit()
                    err = False
        except Exception as e:
            print(e)
            conn = get_conn()
            conn.rollback()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err,t_id


    def article_select_tag(self, t_tags=''):
        '''select article just by tag'''

        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,res = True,()
        sql = 'select * from ec_article'
        if not bool(t_tags):
            sql += ";"
        else:
            sql += " where "
            for tag in t_tags:
                sql += "t_tags like '%%%s%%' and "%tag
            sql = sql[:-5] + ";"
        try:
            cursor.execute(sql)
            rs = cursor.fetchall()
            if bool(rs):
                err,res = False,rs
        except Exception as e:
            print(e)
            conn = get_conn()
            conn.rollback()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err,res



    def article_select(self, t_id):
        '''select article just by t_id'''

        conn = socket_pool.pop()
        cursor = conn.cursor()
        err,res = True,()
        sql = "select * from ec_article where t_id=%r;" % t_id
        try:
            if cursor.execute(sql) == 1:
                rs = cursor.fetchone()
                if bool(rs):
                    err,res = False,rs
        except Exception as e:
            print(e)
            conn = get_conn()
            conn.rollback()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err,res

    def article_del(self, tid):
        '''easy article delete'''

        conn = socket_pool.pop()
        cursor = conn.cursor()
        err = True
        sql = "delete from ec_article where t_id=%r;" % tid
        try:
            st = cursor.execute(sql)
            if st == 1:
                err = False
                conn.commit()
        except Exception as e:
            print(e)
            conn = get_conn()
            conn.rollback()
        finally:
            cursor.close()
            socket_pool.append(conn)
        return err
