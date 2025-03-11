import re
text = "/fesf.json"

res = re.match("^[^\\\/]+?\.[^\\\/]+$", text)
print(res)