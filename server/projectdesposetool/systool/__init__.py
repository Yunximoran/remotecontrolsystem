import os
import platform
from tkinter import filedialog


def choose_software():
    OSN = platform.system()
    if OSN == "Windows":
        filedialog_shell = "start explorer"
    
    if OSN == "Linux":
        filedialog_shell = "nautilus &"
    
    try:
        os.system(filedialog_shell)
    except:
        pass