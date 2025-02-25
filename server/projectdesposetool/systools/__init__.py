
import tkinter
from tkinter import filedialog
import os

from .network import NetWork
from .processing import Pool, Process
from .logger import Logger
from . resolver import Resolver

def choose_file():
    window = tkinter.Tk()
    window.withdraw()
    window.attributes("-topmost", True)
    file_path = filedialog.askopenfilename()
    filename = os.path.basename(file_path)
    print(filename)
    window.quit()
    return filename, file_path