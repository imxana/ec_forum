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
        u_id = ''
        err = True
        cursor = conn.cursor()
        u_id = gene_id()
        while self.userid_search(u_id, table='ec_user'):
            u_id = gene_id()
        sql = "insert into ec_user(u_name, u_email, u_psw, u_id, u_email_confirm, u_level, u_reputation) values('%s','%s','%s',%s,0,4,0);" % (name,email,psw,u_id)
        print(sql)
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

    def userid_search(self, ec_id, table='ec_user'):
        cursor = conn.cursor()
        exist = True
        try:
            sql = "select * from %s where u_id='%s';" % (table,ec_id)
            cursor.execute(sql)
            rs = cursor.fetchone()
            exist = bool(rs)
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return exist

    def signin_select(self, loginname, psw, method='u_name'):
        cursor = conn.cursor()
        err,res = True,()
        try:
            sql = "select * from ec_user where %s='%s' and u_psw='%s';" % (method,loginname,psw)
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

    def sign_del(self, uid, psw):
        cursor = conn.cursor()
        err = True
        sql = "delete from ec_user where u_id='%s' and u_psw='%s';" % (uid,psw)
        print(sql)
        try:
            print(1)
            st = cursor.execute(sql)
            if st == 1:
            #if cursor.execute(sql) == 1:
                print(2)
                err = False
                conn.commit()
        except Exception as e:
            raise e
            conn.rollback()
        finally:
            cursor.close()
        return err




if __name__ == '__main__':
    conn = pymysql.Connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            passwd = '',
            db = 'ec_forum',
            charset = 'utf8'
            )
    # cursor = conn.cursor()
    #
    # sql_insert = "insert into user(userid, username) values(9, 'nanako')"
    # sql_update = "update user set username='nana' where userid=9"
    # sql_delete = "delete from user where userid>8"
    #
    # try:
    #     cursor.execute(sql_insert)
    #     print (cursor.rowcount)
    #
    #     cursor.execute(sql_update)
    #     print (cursor.rowcount)
    #
    #     cursor.execute(sql_delete)
    #     print (cursor.rowcount)
    #
    #     conn.commit()
    # except Exception as e:
    #     print(e)
    #     conn.rollback()
    #
    # cursor.close()
    # conn.close()
