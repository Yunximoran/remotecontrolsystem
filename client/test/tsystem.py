from depend.system import SYSTEM
import psutil, re

ps = SYSTEM._check_soft_status("D:\\Yuncy Moran\\Life\\miHoYo Launcher\\launcher.exe")
for p in ps:
    print(p)