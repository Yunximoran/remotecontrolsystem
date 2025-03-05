from ._logger import Logger


class Manager:
    def __init__(self):
        self.loglevel = 0


    def init_logger(self, name, logfile):
        self.logger = Logger(name, log_file=logfile)