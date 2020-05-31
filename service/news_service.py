from db.news_dao import NewsDao


class NewsService(object):

    @staticmethod
    def get_newslist_by_state_page(news_state, page, num_per_page=10):
        """
        select the news by news state limited by page
        :param news_state: news state
        :param page: which page
        :param num_per_page: how many news need to display in one page
        :return: the news list , if not found return None
        """
        result = NewsDao.get_newslist_by_state_page(news_state, page, num_per_page)
        if len(result) != 0:
            return result
        else:
            return None

    @staticmethod
    def get_news_total_page_by_state(news_state, num_per_page=10):
        total_page =  NewsDao.get_news_total_page_by_state(news_state,num_per_page)
        return total_page

    @staticmethod
    def update_news_state(news_id, news_state):
        NewsDao.update_news_state(news_id, news_state)

