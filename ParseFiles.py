import os
import re
import json
import psycopg2
from psycopg2 import sql
import flat

def parseResult(flattenedResult,headerName):
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
##            dupeCheck = False
##            if re.search(re.compile('r"'+value+'"'),resultVals[key]) is not None:
##                dupeCheck = True
##            if not dupeCheck:
            if isinstance(value,list):
                for vals in value:
                    resultVals[key] = (', ').join([resultVals[key],vals])
            else:
                resultVals[key] = (', ').join([resultVals[key],value])
        else:
            if isinstance(value,list):
                resultVals[key] = (',').join(value)
            else:
                resultVals[key] = value
    return resultVals

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

##try:
##    conn = psycopg2.connect(dbname="fdadata", user="dev_nate", password="7Unholy1", host="fdadata.cebmuf7zemxv.us-east-2.rds.amazonaws.com", port="5432")
##    cur = conn.cursor()
##    print('Successfully connected to fdadata on AWS')
##except psycopg2.Error as e:
##    print (e)
try:
    conn = psycopg2.connect(dbname="fdadata", user="postgres", password="tesser@89", host="192.168.1.111", port="5432")
    cur = conn.cursor()
    print('Successfully connected to fdadata on AWS')
except psycopg2.Error as e:
    print (e)

## Run through all files in database type order.
headers = FileList()
unique = {
    'udi': 'identifiers_id',
    'fivetenk': '',
    'pma': '',
    'recall': '',
    'classification': '',
    'registration': '',
    'event': ''
}
for fileArray in allFiles.outputAll():
    tableName = fileArray[0]
    fileList = fileArray[1]
    headerList = headers.getArray(tableName) # Select the correct headerList to append to
    for index, files in enumerate(fileList): # Run through a database file-by-file
        ## Format the current file to JSON        
        with open('ExtractedZips/{0}'.format(files)) as file:
            jsonFile = json.load(file)
        results = jsonFile["results"]
        
        currentPercent = 0
        for resultIndex, result in enumerate(results):
            ## This section is just for displaying an incrementing percent to show completion status
            percent = round((resultIndex / len(results)) * 100)
            if (currentPercent < percent):
                currentPercent = percent
                print('Sorting data from {0}. Total Files: {1}. {2}% Completed'.format(files, len(results), currentPercent))

                
            flattenedResult = flat.ten(result,tableName) # Get all Key-Value pairs from the file's individual results
            resultVals = parseResult(flattenedResult,tableName)
            
            headersOutput = []
            values = []
            updateSet = ""
            for key, value in resultVals.items():
                headersOutput.append(key)
                
                for allValues in value:
                    allValues = allValues.replace("'","''")
                values.append(value)
                
                foundHeader = False
                for headerValue in headerList:
                    if (key == headerValue):
                        foundHeader = True
                if (not foundHeader):
                    headerList.append(key)                    
                    cur.execute(sql.SQL("ALTER TABLE {0} ADD COLUMN IF NOT EXISTS {1} text;").format(sql.Identifier(tableName),sql.Identifier(key)))
                    print('Updated ' + tableName + ' with new column: ' + key)
                    conn.commit()
            headers = (', ').join((n) for n in headersOutput)
            name = ('{}').format(tableName)
            vals = sql.Composed([sql.SQL(',').join(sql.Literal('%s') for n in values)])
            query = "INSERT INTO {0} ({1}) VALUES ({2});".format(name,headers,(',').join('%s' for n in values))
            cur.execute(query,values)
            
##            cur.execute(sql.SQL("INSERT INTO {0} (%s) VALUES (%s) ON CONFLICT (something) DO UPDATE SET %s;").format(sqlIdentifier(tableName)),[headersOutput,values,updateSet])
        conn.commit()
        file.close()
cur.close()
conn.close()
