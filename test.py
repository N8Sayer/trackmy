import re

pattern = re.compile(r"device-event")
##fileName = '1991q4-device-event-0001-of-0001.json'
fileName = 'device-udi.json'
file1 = re.search(pattern,fileName)

print (file1 is not None)
print (fileName)
