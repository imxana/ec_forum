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
        u_id = ''
        err = True
        cursor = conn.cursor()
        u_id = gene_id()
        while self.userid_search(u_id, table='ec_user'):
            u_id = gene_id()
        sql = "insert into ec_user(u_name, u_email, u_psw, u_id, u_email_confirm, u_level, u_reputation) values('%s','%s','%s',%s,0,4,0);" % (name,email,psw,u_id)
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
        sql = "select * from %s where u_id='%s';" % (table,ec_id)
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

    def user_update(self, info):
        '''update the infomation'''
        cursor = conn.cursor()
        err,res = True,()
        if len(info) == 1:
            return
        sql = "update ec_user set "
        for k,v in info.items():
            sql += "%s=%s,"
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
