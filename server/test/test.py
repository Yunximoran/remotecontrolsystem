from core.depend.control import Control


controlor = Control()


if __name__ == "__main__":
    controlor.sendtoclient([], instructs="hello")