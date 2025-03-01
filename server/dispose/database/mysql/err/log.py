import logging
import colorlog
import os

folder_mysql = "mysql/logs/"
if not os.path.exists(folder_mysql):
    os.makedirs(folder_mysql)


class LogManger:
    def __init__(self, name, attr):
        self.__Init(name)
        self.attr = attr

    def __Init(self, name):
        # 创建日志记录器（getLogger）， 设置日志级别(setLevel)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 创建日志处理器：
        console_handler = logging.StreamHandler()

        file_handler = logging.FileHandler(f"mysql/logs/{name}.log", "w")

        # 设置日志格式、将日志格式添加到日志处理器
        log_format = "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        colors = {
            "DEBUG": 'blue',
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red"
        }
        formatter = colorlog.ColoredFormatter(log_format, log_colors=colors)
        console_handler.setFormatter(formatter)

        # 将日志处理器添加到日志记录器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def getDebug(self, msg):
        """
         获取debug日志
        :param msg: 日志信息
        :return:
        """
        level = 0
        self.logger.debug(f"{msg}\n\tattr: {self.attr}")

    def getInfo(self, msg):
        level = 1
        self.logger.info(f"{msg}\n\tattr: {self.attr}")

    def getWarning(self, msg):
        level = 2
        self.logger.warning(f"{msg}\n\tattr: {self.attr}")

    def getError(self, msg):
        level = 3
        self.logger.error(f"{msg}\n\tattr: {self.attr}")

    def getCritical(self, msg):
        level = 4
        self.logger.critical(f"{msg}\n\tattr: {self.attr}")

    """
    # 使用日志记录器记录日志 (弱 --> 强)
    logger.debug("这是一条debug级别日志")       # 详细信息， 通常只在诊断问题时使用
    logger.info("这是一条info级别日志")         # 确认程序按预期运行
    logger.warning("这是一条warning级别日志")   # 表示有潜在问题，但不会影响程序运行
    logger.error("这是一条error级别日志")       # 表示严重的问题，程序某些功能无法正常运行
    logger.critical("这是一条critical级别日志") # 表示非常严重的问题，程序可能无法继续运行
    """
