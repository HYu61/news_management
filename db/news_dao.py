from db.mysql_db_pool import MysqlDbPool

class NewsDao(object):
    """
    deal with the news table
    """
    __conn = None
    __cursor = None


    @classmethod
    def get_newslist_by_state_page(cls, news_state, page, num_per_page):
        """
        select the news by news state limited by page
        :param news_state: news state
        :param page: which page
        :param num_per_page: how many news need to display in one page
        :return: the news list
        """
        try:
            cls.__conn = MysqlDbPool.get_pool().get_connection()
            cls.__cursor = cls.__conn.cursor()
            sql = ("SELECT n.id, n.title, u.username, n.create_time, n.state "
                   "FROM t_news n JOIN t_user u ON n.editor_id = u.id "
                   "JOIN t_type t ON t.id = n.type_id "
                   "WHERE n.state = %s "
                   "ORDER BY n.create_time DESC, u.username "
                   "LIMIT %s, %s")
            condition = (news_state, (page -1) * num_per_page, num_per_page)
            cls.__cursor.execute(sql, condition)
            return cls.__cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            MysqlDbPool.release(cls.__cursor, cls.__conn)

    @classmethod
    def get_news_total_page_by_state(cls, news_state, num_per_page):
        """
        get the total page according the state and num per page
        :param news_state:
        :param num_per_page:
        :return: the total page
        """
        try:
            cls.__conn = MysqlDbPool.get_pool().get_connection()
            cls.__cursor = cls.__conn.cursor()
            sql = ("SELECT CEILING(COUNT(*)/%s) FROM t_news WHERE state = %s")
            condition = (num_per_page,news_state)
            cls.__cursor.execute(sql, condition)
            return cls.__cursor.fetchone()[0]
        except Exception as e:
            print(e)
        finally:
            MysqlDbPool.release(cls.__cursor, cls.__conn)

    @classmethod
    def update_news_state(cls, news_id, news_state):
        try:
            cls.__conn = MysqlDbPool.get_pool().get_connection()
            cls.__conn.start_transaction()
            cls.__cursor = cls.__conn.cursor()
            sql = ("UPDATE t_news SET state = %s WHERE id = %s")
            condition = (news_state, news_id)
            cls.__cursor.execute(sql, condition)
            cls.__conn.commit()
        except Exception as e:
            cls.__conn.rollback()
            print(e)
        finally:
            MysqlDbPool.release(cls.__cursor, cls.__conn)


    @classmethod
    def get_all_news_list(cls, page, num_per_page):
        try:
            cls.__conn = MysqlDbPool.get_pool().get_connection()
            cls.__conn = cls.__conn.cursor()
            sql = ("SELECT ")
        except Exception as e:
            print(e)
        finally:
            MysqlDbPool.release(cls.__cursor, cls.__conn)


    @classmethod
    def insert_news(cls, index):
        try:
            cls.__conn = MysqlDbPool.get_pool().get_connection()
            cls.__conn.start_transaction()
            cls.__cursor = cls.__conn.cursor()
            sql = ("INSERT INTO `t_news` VALUES(%s, %s, '2', '1', '1', '1', '2018-11-22 18:55:56', '2018-11-22 18:55:56', 'pending')")
            title = "title - {}".format(index)
            condition = (index, title)
            cls.__cursor.execute(sql, condition)
            cls.__conn.commit()
        except Exception as e:
            cls.__conn.rollback()
            print(e)
        finally:
            MysqlDbPool.release(cls.__cursor, cls.__conn)



if __name__ == "__main__":
    NewsDao.update_news_state(1, "drft")
    print(NewsDao.get_newslist_by_state_page("pending", 1,3))
    print(NewsDao.get_news_total_page_by_state("pending", 2))


    for i in range(4, 25):
        NewsDao.insert_news(i)