import re
text = "e"

s = re.match("^(3|e|(error))$", text)

print(s)