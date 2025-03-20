import re

pattern = r'^https?://'  # 协议头
pattern += r'(?:'  # 开始分组
pattern += r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,3}'  # 域名部分（如 example.com）
pattern += r'|'  # 或
pattern += r'(?:\d{1,3}\.){3}\d{1,3}(?::\d{2,5})?'  # IPv4地址 + 可选端口
pattern += r')'  # 结束分组
pattern += r'/?$'  # 可选的末尾斜杠

regex = re.compile(pattern)

print(regex)