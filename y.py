from db.user_dao import UserDao

print(UserDao.login("admin", "123456"))
r = UserDao.search_user_role("admin")
print(r)


