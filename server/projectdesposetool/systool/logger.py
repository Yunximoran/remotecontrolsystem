import logging
from logging.handlers import RotatingFileHandler
import os

class Logger:
    CWD = os.getcwd()
    def __init__(self, name, log_file='.log', level=logging.INFO, max_bytes=10485760, backup_count=5):
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
        log_dir = os.path.join(self.CWD, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_file)
        
        # 创建日志格式器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 创建滚动文件处理器
        file_handler = RotatingFileHandler(
            log_path, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)
