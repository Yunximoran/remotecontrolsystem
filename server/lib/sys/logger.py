import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path


WROKDIR = Path.cwd()
LOGDIR = WROKDIR.joinpath("logs")
LOGDIR.mkdir(parents=True, exist_ok=True)
LEVEL = logging.INFO
IFCONSOLE = False

class Logger:
    # 日志管理器只在despose中使用吗？
    CWD = os.getcwd()
    def __init__(self, name, log_file='.log', level=LEVEL,
                 max_bytes=10485760, backup_count=5):
        """
        name: 日志记录器名称（通常使用模块名__name__）
        log_file: 日志文件名（默认app.log）
        level: 日志级别（默认INFO）
        max_bytes: 单个日志文件最大字节数（默认10MB）
        backup_count: 保留的备份文件数量（默认5个）
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 创建日志目录（如果不存在）
        log_path = LOGDIR.joinpath(log_file)
        log_path.touch()


        
        # 创建日志格式器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if IFCONSOLE:
            self.addconsole(formatter)
        
        # 创建滚动文件处理器
        file_handler = RotatingFileHandler(
            log_path, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def addconsole(self, formatter):
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def format_logtext(self, *msgs, **dmsgs):
        """
            格式化日志文本
        """
        logtext = []
        logtext.append("\t".join(msgs))
        
        for msg in dmsgs:
            item = f"{msg}: {dmsgs[msg]}"
            logtext.append(item)
        
        return "\n".join(logtext)
    
    def record(self, level:int , msg: str):
        """
            日志记录器：执行写入操作
        log level: debug < info < waring < error < critical
        """
        if level == 0:
            self.__debug(msg)
        elif level == 1:
            self.__info(msg)
        elif level == 2:
            self.__warning(msg)
        elif level == 3:
            self.__error(msg)
        elif level == 4:
            self.__critical(msg)
        else:
            raise ValueError("must range 0, 4 the attribute level")
    
    def __debug(self, message):
        self.logger.debug(message)
    
    def __info(self, message):
        self.logger.info(message)
    
    def __warning(self, message):
        self.logger.warning(message)
    
    def __error(self, message):
        self.logger.error(message)
    
    def __critical(self, message):
        self.logger.critical(message)


if __name__ == "__main__":
    logger = Logger("logtext", log_file="logtext.log")
    logtext = logger.format_logtext("t1", "t2", a1 = __file__, a2 = __name__)
    print(logtext)
    logger.record(4, "hello wrold")