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


