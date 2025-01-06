import multiprocessing


class NoDaemonProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False

    def _set_daemon(self):
        pass
    
    daemon = property(_get_daemon, _set_daemon)
    

class Pool(multiprocessing.Pool):
    Process = NoDaemonProcess