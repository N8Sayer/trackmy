import urllib.request
import json
import zipfile
import os
import re
import pprint

url = 'https://api.fda.gov/download.json'
newData = urllib.request.urlretrieve(url,'./urllist.txt')

with open('./urllist.txt') as newData:
    newData = json.load(newData)
if (os.path.exists('./oldlist.txt')):
    with open('./oldlist.txt') as oldData:
        oldData = json.load(oldData)
else:
    oldData = [];

classification = newData["results"]["device"]["classification"]["partitions"][0]["file"]
fivetenk = newData["results"]["device"]["510k"]["partitions"][0]["file"]
recall = newData["results"]["device"]["recall"]["partitions"][0]["file"]
pma = newData["results"]["device"]["pma"]["partitions"][0]["file"]
registration = newData["results"]["device"]["registrationlisting"]["partitions"][0]["file"]
adverse = newData["results"]["device"]["registrationlisting"]["partitions"][0]["file"]
udi = []
for partitions in newData["results"]["device"]["udi"]["partitions"]:
    udi.append(partitions["file"])
adverse = []
for partitions in newData["results"]["device"]["event"]["partitions"]:
    adverse.append(partitions["file"])

if (len(oldData) is 0 or oldData["results"]["device"]["classification"]["export_date"] != newData["results"]["device"]["classification"]["export_date"]):
    print('Downloading 1 file from Classification API')
    urllib.request.urlretrieve(classification, './classification.zip')
    print('Finished downloading Classification API data')
else:
    print('Classification API data is up to date')

if (len(oldData) is 0 or oldData["results"]["device"]["510k"]["export_date"] != newData["results"]["device"]["510k"]["export_date"]):
    print('Downloading 1 file from 510k API')
    urllib.request.urlretrieve(fivetenk, './510k.zip')
    print('Finished downloading 510k API data')
else:
    print('510k API data is up to date')
    
if (len(oldData) is 0 or oldData["results"]["device"]["recall"]["export_date"] != newData["results"]["device"]["recall"]["export_date"]):
    print('Downloading 1 file from Recall API')
    urllib.request.urlretrieve(recall, './recall.zip')
    print('Finished downloading Recall API data')
else:
    print('Recall API data is up to date')
    
if (len(oldData) is 0 or oldData["results"]["device"]["pma"]["export_date"] != newData["results"]["device"]["pma"]["export_date"]):
    print('Downloading 1 file from PMA API')
    urllib.request.urlretrieve(pma, './pma.zip')
    print('Finished downloading PMA API data')
else:
    print('PMA API data up to date')

if (len(oldData) is 0 or oldData["results"]["device"]["registrationlisting"]["export_date"] != newData["results"]["device"]["registrationlisting"]["export_date"]):
    print('Downloading 1 file from Registration API')
    urllib.request.urlretrieve(registration, './registration.zip')
    print('Finished downloading Registration API data')
else:
    print('Registration API data is up to date')
    
if (len(oldData) is 0 or oldData["results"]["device"]["udi"]["export_date"] != newData["results"]["device"]["udi"]["export_date"]):
    for index, files in enumerate(udi):
        print('Downloading file {0} of {1} from UDI API'.format(index+1, len(udi)))
        filename = re.search(r"\w+-\w+-\w+-\w+-\w+.json.zip$", files)
        urllib.request.urlretrieve(files, './{0}'.format(filename.group()))
    print('Finished downloading {0} files from UDI API'.format(len(udi)))
else:
    print('UDI API data is up to date')

if (len(oldData) is 0 or oldData["results"]["device"]["event"]["export_date"] != newData["results"]["device"]["event"]["export_date"]):
    for index, files in enumerate(adverse):
        print('Downloading file {0} of {1} from Adverse Event API'.format(index+1, len(adverse)))
        filename = re.search(r"(\w+)/\w+-\w+-\w+-\w+-\w+.json.zip$", files)
        split = re.split('/',filename.group())
        urllib.request.urlretrieve(files, './{0}'.format(split[0]+'-'+split[1]))
    print('Finished downloading {0} files from Adverse Event API'.format(len(adverse)))
else:
    print('Adverse Event API data is up to date')

os.replace('./urllist.txt', './oldlist.txt')
