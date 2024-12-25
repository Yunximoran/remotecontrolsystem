# import subprocess
# import ctypes
# import sys
# import os

# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False
    
# if is_admin():
#     print("admin")
# else:
#     # ShellExecuteW
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#     sys.exit(0)
# print(os.getcwd())
# basepath = os.getcwd()
# topath = "local\softwares"
# print(os.path.join(basepath, topath, "geek"))
# subprocess.Popen(['mklink',  topath+"\\geek", r"D:\\toolkit\\system\\geek.exe"], shell=True)


import ctypes
import string

def get_drives():
    drives = []
    bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
    print(f"Initial bitmask: {bin(bitmask)}")  # 打印初始的bitmask值

    for letter in string.ascii_uppercase:
        print(f"Checking drive {letter}:\\")  # 打印正在检查的驱动器
        if bitmask & 1:
            drives.append(f"{letter}:\\")
            print(f"Drive {letter}:\\ added to drives list.")  # 打印添加到列表的驱动器
        bitmask >>= 1
        print(f"Bitmask after shift: {bin(bitmask)}")  # 打印位移后的bitmask值

    return drives

print(get_drives())
