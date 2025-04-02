import os
from pathlib import Path

results = []
check_object = "哔哩哔哩"
_disks =[Path("D:\\")]
for disk in _disks:
    for root, dirs, files in os.walk(disk):
        for file in files:
            if file == check_object:
                results.append(os.path.join(root, file))
        for dir in dirs:
            if dir == check_object:
                results.append(os.path.join(root, dir))    
print(results)