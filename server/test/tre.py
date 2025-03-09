import re
text = "WindowsLinux"

s = re.match("^(Windows)$|^(Linux)$|^(MacOS)$", text)

print(s)