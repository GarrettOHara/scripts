import re

string = "2022-05-28 03:01:24.071000+00:00"

print(re.sub("\+(.*)","",string ))
