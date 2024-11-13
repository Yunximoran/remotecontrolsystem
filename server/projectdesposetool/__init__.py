
from fastapi import HTTPException

from .parse import CONFIG
from .start_server import SERVERMANAGE


def CheckLoginInfomation(username, password):
    return True
    # return True if username == "admin" and password == "123456" else False
    
