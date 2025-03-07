from depend.system import SYSTEM


# SYSTEM.restart()

import psutil, re, time



d = {}
s = psutil.process_iter()
# SYSTEM.start_software("DarkDominance")
for item in s:
    # print(item.pid)
    # item.exe()
    if re.match("DarkDominance", item.name()):
        print(item.exe())
        # try:
        #     # exe = psutil.Process(item.pid).exe()
        #     print(item.exe())
        # except psutil.NoSuchProcess:
        #     print("无进程")
        # except psutil.AccessDenied:
        #     print("无权限")
#     # print(item.name)
#     if item.name() not in d.keys():
#         d[item.name()] = 0
#     else:
#         d[item.name()] += 1
#     # print(item)
    
# for item in d:
#     print(item, d[item])
    
time.sleep(10)
SYSTEM.close_software("DarkDominance", f"E:\Materail\game material\HA\DarkDominance.exe")