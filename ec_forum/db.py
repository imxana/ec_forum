# coding:utf8
import pymysql



class sqlQ(object):

    def signup_insert(self,name,email,psw):
        err = True
        cursor = conn.cursor()
        try:
            sql = "insert into ec_user(u_name,u_email,u_psw) values(%s,%s,%s);" % (name,email,psw)
            cursor.execute(sql)
            if cursor.rowcount != 1:
                raise Exception('sign_up failed')
                err = False
        except Exception as e:
            raise e
            err = False
        finally:
            cursor.close()
        return True

    def signup_select(self, name, psw=''):
        cursor = conn.cursor()
        try:
            sql = "select * from ec_user where ec_name=%s"
            cursor.execute(sql)
        except Exception as e:
            raise(e)
        finally:
            cursor.close()

    def userid_search(self, id):
        cursor = conn.cursor()
        try:
            pass
        except Exception as e:
            raise e
        finally:
            pass

    def sign_select():

        pass

    def selectAll():
        pass

    def delete():
        pass




if __name__ == '__main__':
    # conn = pymysql.Connect(
    #         host = '127.0.0.1',
    #         port = 3306,
    #         user = 'root',
    #         passwd = '',
    #         db = 'test',
    #         charset = 'utf8'
    #         )
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