import ctypes
import string
import os

def get_disks():
    drives = []
    bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives

if __name__ == "__main__":
    import subprocess
    
    source = r".\local\softwares"
    # E:\Materail\game material\Chapter01テスト展示版
    
    s = os.path.dirname("E:\Materail\game material\Chapter01テスト展示版")
    print(s)