# 匹配URL地址
HTTP = r"^https?://"

# 匹配IP地址
IP = r"^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$"

# 匹配mac地址
MAC = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"


if __name__ == "__main__":
    import re
    print(re.match(IP, "192.168.31.176"))