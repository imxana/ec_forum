# coding:utf8
import pymysql
from ec_forum.id_dealer import gene_id


class sqlQ(object):

    def signup_insert(self,name,email,psw):
        u_id = ''
        err = True
        cursor = conn.cursor()
        try:
            u_id = gene_id()
            while self.id_search(u_id):
                u_id = gene_id() 
            sql = "insert into ec_user(u_name, u_email, u_psw, u_id, u_email_confirm, u_level, u_reputation) values(%s,%s,%s,%s,0,4,0);" % (name,email,psw,u_id)
            cursor.execute(sql)
            if cursor.rowcount == 1:
                # suc!!
                err = False
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return err, u_id

    def signup_select(self, name, method='u_name'):
        cursor = conn.cursor()
        exist = True
        try:
            sql = "select * from ec_user where %s=%s" % (method,name)
            cursor.execute(sql)
            rs = cursor.fetchone()
            if rs == ()
               exist = False
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return exist

    def id_search(self, ec_id, table='ec_user'):
        cursor = conn.cursor()
        exist = True
        try:
            sql = "select * from %s where u_id=%s" % (table,ec_id)
            cursor.execute(sql)
            rs = cursor.fetchone()
            if rs == ()
               exist = False
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return exist

    def signin_select(self, loginname, method='u_id'):
        cursor = conn.cursor()
        err = True
        info = ()
        try:
            sql = "select * from %s where %s=%s" % (u_id, loginname)
            cursor.execute(sql)
            rs = cursor.fetchone()
            if rs =! ()
                err = False
                info = rs
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return err, info


    def selectAll():
        pass

    def delete():
        pass




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
