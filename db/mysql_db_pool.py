import mysql.connector.pooling
import mysql.connector


class MysqlDbPool(object):
    __config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "root",
        "database": "news"
    }

    @classmethod
    def get_pool(cls):
        """
        get the database pool
        :return: the database connection pool
        """
        try:
            return mysql.connector.pooling.MySQLConnectionPool(pool_size=5, **cls.__config)
        except Exception as e:
            print(e)

    @classmethod
    def release(cls, *args):
        """
        close the cursor object and connection object
        :param args: the cursor and connection which needed to be closed
        """
        for item in args:
            if isinstance(item, mysql.connector.pooling.PooledMySQLConnection) \
                    or isinstance(item, mysql.connector.cursor.MySQLCursor):
                item.close()

