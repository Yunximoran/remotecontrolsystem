from pymysql import err

from .basic.connector import Connector
from .basic.information import Information
from .tools.construction import Construction
from .tools.formation import FormatPackage
from .tools.check import Check
from .err.log import LogManger




log = LogManger("client", "yumodb.mysql.client")


def luger(func):
    def execLog(*args, **kwargs):
        try:
            func(*args, **kwargs)
            log.getInfo(f"execute success {args[-1]}")
        except err.OperationalError as e:
            log.getError(f"execute error {args[-1]}\n {e}")

    return execLog


class WorkBench(Connector):
    # 是否需要将代码更加基础化
    SQL = Construction()
    Format = FormatPackage()
    check = Check()
    info = Information()

    def init(self, db=None):
        # 重新选择数据库，并初始化
        self.__init__(db)

    def __init__(self, db=None):
        self.__db = db
        self.__tb = None
        super().__init__(self.__db)

    def drop(self, db):
        self.__execute(self.SQL.drop(db))

    def use(self, db):
        self.__db = db
        self.getConn().select_db(db)

    def show(self, isDB=True):
        self.__execute(self.SQL.show(isDB=isDB))
        return self.__getData()

    def cdb(self, dbn, isExists=False):
        self.__execute(self.SQL.ndb(dbn, isExists=isExists))

    def ctb(self, tbn, targets, primary=None, unique=None):
        self.__execute(self.SQL.create(tbn, targets, primary, unique))

    def insert(self, tbn, data, ignore=False):
        """
            执行插入操作
        :param tbn: 表名
        :param data: 代插入数据
        :param ignore: 是否忽略重复值
        :return:
        """
        # 如果vals返回空则说明插入单条数据或数据格式错误
        if isinstance(data, dict):  # 根据数据类型，执行对应的格式化操作
            vals, keys = self.Format.formatDict(data)
        else:
            vals, keys = self.Format.formatSeries(data)

        if vals:  # 格式化方法返回，vals,keys两个变量
            for val in vals:
                self.__execute(self.SQL.insert(tbn, val, keys, ignore=ignore))
        else:  # 如果vals为空，说明数据存在错误
            raise 'DataError'
            # try:
            #     vals = tuple(data.values())
            #     self.__execute(self.SQL.insert(tbn, vals, keys, ignore=ignore))
            # except AttributeError:
            #     vals = tuple(data)
            #     self.__execute(self.SQL.insert(tbn, vals, keys, ignore=ignore))

    def update(self, tbn,
               newData=None,
               **kwargs):
        """
            更新数据
        :param tbn: 表名
        :param newData:
        :param kwargs:
        :return:
        """
        # update 方法应该可以参考insert方法，更新单条数据或者多条数据， 对于update 指定键 和 指定条件 是必须的
        # 要不要做多样化输入数据
        # 指定条件是必须得， 但不是手动输入条件， 给定一条数据， 通过其中某键为索引定位数据更新
        # update方法将以什么形式更新
        # 更新需要换新的整条数据
        # 除了字典也可以是可便利对象，单条数据插入，多数据插入
        # 分开执行，单次更新：字典、元组。 多次更新：字典、元组
        # 尝试参考insert参数，但是update必须有keys索引来构建condition
        if (newData and kwargs) or (not newData and not kwargs):
            return

        if newData:
            vals, keys = self.Format.formatDict(newData)
        else:
            vals, _ = self.Format.formatSeries(kwargs['vals'])
            keys = tuple(kwargs['keys'])
        isOnce = self.check.checkInsertOnce(vals)  # 判断是否为单次更新
        if isOnce:
            condition = self.__updateGetCondition(tbn, vals, keys)
            self.__execute(self.SQL.update(tbn, vals, keys, condition=condition))
        else:
            for val in vals:
                condition = self.__updateGetCondition(tbn, val, keys)
                self.__execute(self.SQL.update(tbn, val, keys, condition=condition))

    def __updateGetCondition(self, tbn, vals, keys):
        # 年少不知元组好
        for key in keys:
            if self.check.isPRI(self.__db, tbn, key):
                pri = key
                index = keys.index(key)
                return f"{pri} = {vals[index]}"
            if self.check.isUNI(self.__db, tbn, key):
                uni = key
                index = keys.index(key)
                return f"{uni} = {vals[index]}"
        return f"{keys[0]} = {vals[0]}"

    def delete(self, tbn, **condition):
        keys = condition.keys()
        vals = condition.values()
        for key, val in zip(keys, vals):
            self.__execute(self.SQL.delete(tbn, f"{key} = {val}"))

    def __deleteGetCondition(self, condition):
        pass

    def select(self, tbn, findKey="*", condition=None):
        self.__execute(self.SQL.select(tbn, findKey, condition))
        return self.__getData()

    def alter(self, tbn,
              rename=None,
              column=None,
              primary=None,
              unique=None):
        pass

    @luger
    def __execute(self, SQL):
        # self.getCursor().execute(SQL)
        try:
            self.getCursor().execute(SQL)
            log.getInfo(f"execute success {SQL}")
        except err.OperationalError as e:
            log.getError(f"execute error {SQL} \n {e}")

    def __rollback(self):
        self.getConn().rollback()

    def __getData(self):
        results = self.getCursor().fetchall()
        return tuple([row if len(row) > 1 else row[0] for row in results])

    @staticmethod
    def version():
        return "1.0.0"

    def getUsingDB(self):
        return self.__db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


"""
`ALTER` 是 MySQL 中用于修改数据库对象（如表、列、索引等）的命令。以下是 `ALTER` 的一些常见用法：

1. 修改表名：

```
ALTER TABLE old_table_name RENAME TO new_table_name;
```

2. 修改表的字符集：

```
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4;
```

3. 修改表的存储引擎：

```
ALTER TABLE table_name ENGINE = InnoDB;
```

4. 添加列：

```
ALTER TABLE table_name ADD COLUMN column_name column_definition;
```

5. 修改列：

```
ALTER TABLE table_name MODIFY COLUMN column_name new_column_definition;
```

6. 重命名列：

```
ALTER TABLE table_name CHANGE COLUMN old_column_name new_column_name new_column_definition;
```

7. 删除列：

```
ALTER TABLE table_name DROP COLUMN column_name;
```

8. 添加主键：

```
ALTER TABLE table_name ADD PRIMARY KEY (column_name);
```

9. 删除主键：

```
ALTER TABLE table_name DROP PRIMARY KEY;
```

10. 添加外键：

```
ALTER TABLE table_name ADD CONSTRAINT constraint_name FOREIGN KEY (column_name) REFERENCES another_table(another_column)
```
"alter table test_db add constraint constraint_name foreign key(id) references another_table()"

11. 删除外键：

```
ALTER TABLE table_name DROP FOREIGN KEY constraint_name;
```

12. 添加索引：

```
ALTER TABLE table_name ADD INDEX index_name (column_name);
```

13. 删除索引：

```
ALTER TABLE table_name DROP INDEX index_name;
```

注意：在使用 `ALTER` 命令时，需要具有对数据库对象足够的权限。


"""
