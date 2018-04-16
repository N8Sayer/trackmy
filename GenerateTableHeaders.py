import os
import re
import json
import psycopg2
from psycopg2 import sql
import flat

udi_pattern = re.compile(r"^device-udi")
fivetenk_pattern = re.compile(r"^510k")
pma_pattern = re.compile(r"^pma")
recall_pattern = re.compile(r"^recall")
classification_pattern = re.compile(r"^classification")
registration_pattern = re.compile(r"^registration")
event_pattern = re.compile(r"device-event")

class FileList:
    def __init__(self):
        self.udi = []
        self.fivetenk = []
        self.pma = []
        self.recall = []
        self.classification = []
        self.registration = []
        self.event = []
    def getArray(self, arrayName):
        return getattr(self, arrayName)
    def outputAll(self):
        return [
            ['udi', self.udi],
            ['fivetenk', self.fivetenk],
            ['pma', self.pma],
            ['recall', self.recall],
            ['classification', self.classification],
            ['registration', self.registration],
            ['event',self.event]
        ]

allFiles = FileList()
for files in os.listdir('./ExtractedZips'):
    if (re.match(udi_pattern, files) is not None):
        allFiles.udi.append(files)
    elif (re.match(fivetenk_pattern, files) is not None):
        allFiles.fivetenk.append(files)
    elif (re.match(pma_pattern, files) is not None):
        allFiles.pma.append(files)
    elif (re.match(recall_pattern, files) is not None):
        allFiles.recall.append(files)
    elif (re.match(classification_pattern, files) is not None):
        allFiles.classification.append(files)
    elif (re.match(registration_pattern, files) is not None):
        allFiles.registration.append(files)
    elif (re.search(event_pattern, files) is not None):
        allFiles.event.append(files)
print('Files parsed')

headers = FileList()
if (os.path.exists('./headers.txt')):
    os.remove('headers.txt')
headerFile = open('headers.txt','w+')
for fileArray in allFiles.outputAll():
    headerName = fileArray[0]
    fileList = fileArray[1]
    for index, files in enumerate(fileList):
        if (index == 0):
            with open('ExtractedZips/{0}'.format(files)) as file:
                jsonFile = json.load(file)
            results = jsonFile["results"] 
            currentPercent = 0
            for resultIndex, result in enumerate(results):
                percent = round((resultIndex / len(results)) * 100)
                if (currentPercent < percent):
                    currentPercent = percent
                    print('Sorting data from {0}. Total Files: {1}. {2}% Completed'.format(files, len(results), currentPercent))
                    
                headerList = headers.getArray(headerName)
                flattenedResult = flat.ten(result,headerName)
                resultVals = {}
                for key,value in flattenedResult:
                    split = list(filter(None,re.split(r",",key)))
                    arrayPosition = -1
                    for stringIndex,strings in enumerate(split):
                        try:
                            intCheck = int(strings)
                        except:
                            intCheck = strings
                        if isinstance(intCheck,int):
                            arrayPosition = stringIndex

                    if arrayPosition >= 0:
                        if (arrayPosition + 1) != (len(split) - 1):
                            key = split[len(split)-2] + '_' + split[len(split)-1]
                        else:
                            key = split[arrayPosition - 1] + '_' + split[arrayPosition + 1]
                    else:
                        if split[len(split)-2] != headerName:
                            key = split[len(split)-2] + '_' + split[len(split)-1]
                        else:
                            key = split[len(split)-1]                            
                            
                    if key in resultVals:
                        dupeCheck = False
                        for vals in resultVals[key]:
                            if vals == value:
                                dupeCheck = True
                        if not dupeCheck:
                            resultVals[key].append(value)
                    else:
                        resultVals[key] = [value]                
                for key,value in resultVals.items():
                    attrHeader = key
                    foundHeader = False
                    for headerValue in headerList:
                        if (attrHeader == headerValue):
                            foundHeader = True
                    if (not foundHeader):
                        headerList.append(attrHeader)
    headerFile.write(headerName + ':\n')
    for header in headers.getArray(headerName):
        headerFile.write(header + '\n')
    headerFile.write('\n\n')
    file.close()
headerFile.close()
