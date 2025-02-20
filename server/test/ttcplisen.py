import time
from core.depend.protocol.tcp import Listener
from projectdesposetool.systool.processing import Process

def S():
    listener = Listener(("127.0.0.1", 8000), 5)
    listener.listen()
if __name__ == "__main__":
    Process(target=S).start()