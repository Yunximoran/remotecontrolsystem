from .config import HOST, PORT, USER, PASSWORD

from pymysql import connect

class Connector:

    def __init__(self, database=None):
        self.__test = "私有成员继承效果测试"
        self.__conn = connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=database,
            autocommit=True
        )
        self.__cursor = self.__conn.cursor()

    def __call__(self, *args, **kwargs):
        return "Hello World!"

    def getConn(self):
        return self.__conn

    def getCursor(self):
        return self.__cursor

    def close(self):
        self.__conn.close()
        self.__cursor.close()
