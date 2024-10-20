import os
import sys
from pathlib import Path


def find_software(filename, search_path):
    l = []
    for root, dirs, files in os.walk(search_path):
        if filename in files or search_path in dirs:
            print(f"找到文件{filename}")
            p = os.path.join(root, filename)
            l.append(p)
    return l


data = find_software("launcher.exe", "C:\\")

print(data)