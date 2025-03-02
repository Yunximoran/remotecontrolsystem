# 获取数据库信息类
# client是否继承information，我期望他可以独立工作

from .connector import Connector
from ..err.log import LogManger


log = LogManger("Information", "yumodb.mysql.basic.Information")


# 我需要information可以获取client当前信息，比如当前使用的数据库
# 好像不需要考虑获取数据库，应为我当前使用的数据是可以确定的
# 在没指定数据库是，几乎大部分代码都会出错，
# 但是，information类是独立的信息查询工具。
# 需要将information与client链接起来。
# 获取可以将这部分代码交由其他模块编写，但是感觉这样违背了这个类创建的初衷
class Information:
    __db = None
    __tb = None

    def __init__(self):
        connector = Connector()
        self.__conn = connector.getConn()
        self.__cursor = connector.getCursor()

    def __execute(self, sql):
        log.getInfo(f"execute success {sql}")
        self.__cursor.execute(sql)

    def __getResult(self) -> tuple[tuple]:
        results = self.__cursor.fetchall()
        return results

    def set_db(self, db) -> None:
        self.__db = db

    def set_tb(self, tb) -> None:
        self.__tb = tb

    def getVersion(self):
        return self.__getResult

    def getDataBases(self) -> tuple:
        self.__execute("show databases")
        return tuple([db[0] for db in self.__getResult()])

    def getTables(self, db) -> tuple:
        self.__execute(f"select table_name from information_schema.tables where table_schema = '{db}'")
        return tuple([table[0] for table in self.__getResult()])

    def getColumns(self, db, tb) -> (dict, int):
        """
            获取指定数据库中某个表的字段信息
        :param db: 数据库名
        :param tb: 表名
        :return: results, num
        :return type: dict
        """
        # 获取字段数
        self.__execute(
            f"select column_name, data_type, column_key from information_schema.columns"
            f" where table_schema='{db}' and table_name='{tb}'")
        results = {column_name: (data_type, column_type) for column_name, data_type, column_type in self.__getResult()}
        num = len(results)
        return results, num

    def getCounts(self, db, tb):
        # 统计表中元素
        self.__execute(f"select count(*) from {db}.{tb}")
        count = self.__getResult()
        return count[0][0]

    def getPrimary(self, db, tb):
        columns, keyNum = self.getColumns(db, tb)
        res = []
        for column in columns.keys():
            if columns[column][-1] == "PRI":
                res.append(column)

        return res

    def getUnique(self, db, tb):
        columns, keyNum = self.getColumns(db, tb)
        res = []
        for column in columns.keys():
            if columns[column][-1] == "UNI":
                res.append(column)
        return res


