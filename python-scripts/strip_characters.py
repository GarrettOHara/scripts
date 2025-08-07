import datetime

test_str = "off_topic:hello_world"
print(test_str)
mystr = test_str.split(':')
print(mystr[1])

print(datetime.datetime.now(datetime.timezone.utc))

mystr = ""

if mystr is not "":
    print("we entered the if statement")
else:
    print("we went to else")
