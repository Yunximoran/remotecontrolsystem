import os
import platform
import tkinter
from tkinter import filedialog

def choose_software():
    window = tkinter.Tk()
    window.withdraw()
    window.attributes("-topmost", True)
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("software", ".exe"),
            ("software", "*.docx")
        ]
    )
    window.quit()
    return file_path
    
    
    