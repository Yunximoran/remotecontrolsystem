import logging
import os


from .parse import Parse
from .start_server import SERVERMANAGE



class LogManage:
    def __init__(self, level=logging.INFO, filename=None, savedir=None):
        self.level = level
        self.savedir = savedir
        self.filename = filename
    
    def init(self):
        if not os.path.exists(self.filename):
            os.makedirs(self.filename)
        
    
    def info(self):
        logging.info("the info")
    
    def debug(self):
        logging.debug("the debug")
    
    def warning(self):
        logging.warning("the warning")
    
    def error(self):
        logging.error("the error")
    
    def critical(self):
        logging.critical("the critical")


Parse = Parse()
LogManage = LogManage(savedir=Parse.CWD)


# logging.basicConfig(
#     level=logging.INFO,
#     filename='logs/ProjectDespose.log'
# )

# logger = logging.getLogger(__name__)
# logger.info('the message')
# logger.critical()