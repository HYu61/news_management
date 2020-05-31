from db.user_dao import UserDao

class UserService(object):

    @staticmethod
    def login(username, password):
        """
        find wether the user exist in the database
        :param username: username
        :param password: password
        :return: True if the user and password are all corrected, False, if one of them is not correct
        """
        return UserDao.login(username, password)

    @staticmethod
    def search_user_role(username):
        """
        get the urser's role
        :param username: the user's username
        :return: the user's role if not found, return None
        """
        return UserDao.search_user_role(username)