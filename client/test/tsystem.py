# from depend.system import SYSTEM


# # SYSTEM.restart()

# import psutil, re, time

from depend.system import SYSTEM



SYSTEM.start_software("D:\\toolkit\\system\\geek.exe")

a  = SYSTEM._check_soft_status("geek", "D:\\toolkit\\system\\geek.exe")
print(a)