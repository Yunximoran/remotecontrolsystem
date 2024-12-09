import ctypes
import string

def get_disks():
    drives = []
    bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives

if __name__ == "__main__":
    disks = get_disks()
    print("磁盘数量:", len(disks))
    print("磁盘列表:", disks)
