from db.mysql_db_pool import MysqlDbPool


class UserDao(object):
    """
    deal with t_user table
    """
    __conn = None
    __cursor = None

    @classmethod
    def login(cls,username, password):
        """
        find wether the user exist in the database
        :param username: username
        :param password: password
        :return: True if the user and password are all corrected, False, if one of them is not correct
        """
        try:
            cls.__conn = MysqlDbPool.get_pool().get_connection()
            cls.__cursor = cls.__conn.cursor()
            sql = (
                "SELECT COUNT(*) FROM t_user WHERE username = %s AND AES_DECRYPT(UNHEX(password), 'HelloWorld') = %s")
            cls.__cursor.execute(sql, (username, password))
            result = cls.__cursor.fetchone()[0]
            return True if result == 1 else False
        except Exception as e:
            print(e)
        finally:
            MysqlDbPool.release(cls.__cursor, cls.__conn)

    @classmethod
    def search_user_role(cls,username):
        """
        get the user's role
        :param username: the user's username
        :return: the user's role if not found, return None
        """
        try:
            cls.__conn = MysqlDbPool.get_pool().get_connection()
            cls.__cursor = cls.__conn.cursor()
            sql = ("SELECT r.role FROM t_user u JOIN t_role r ON u.role_id = r.id WHERE u.username = %s")
            cls.__cursor.execute(sql, (username,))
            result = cls.__cursor.fetchone()
            if result is not None:
                result = result[0]
            return result
        except Exception as e:
            print(e)
        finally:
            MysqlDbPool.release(cls.__conn, cls.__cursor)
