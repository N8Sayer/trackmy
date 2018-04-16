import os
import re
import json
import psycopg2

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
##    def concatAll(self):
##        l = [self.udi,self.fivetenk,self.pma,self.recall,self.classification,self.registration]
##        return [item for sublist in l for item in sublist]

try:
    conn = psycopg2.connect(dbname="fdadata", user="dev_nate", password="7Unholy1", host="fdadata.cebmuf7zemxv.us-east-2.rds.amazonaws.com", port="5432")
    cur = conn.cursor()
    print('Successfully connected to fdadata')
except psycopg2.Error as e:
    print (e)

headerList = ['udi','fivetenk','pma','recall','registration','classification','event']
headerData = FileList()

with open('headers.txt') as headerFile:
    headerOutput = []
    for index,lines in enumerate(headerFile):
        headerOutput.append(lines)
        
    for headers in headerList:
        sectionEnd = False
        sectionStart = 0
        sectionCheck = False
        for index,lines in enumerate(headerOutput):
            if (lines == (headers +':\n')):
                sectionStart = index
                sectionCheck = True
            if (not sectionEnd and sectionCheck and lines is '\n'):
                sectionEnd = True
            if (not sectionEnd and index > sectionStart and sectionCheck):                
                headerData.getArray(headers).append(lines[0:len(lines)-1])

for allHeaders in headerData.outputAll():
    headerOutput = ""
    for index,headerList in enumerate(allHeaders[1]):
        if (index < len(allHeaders[1])-1):
            headerOutput += headerList + ' text, '
        else:
            headerOutput += headerList + ' text'
    cur.execute("CREATE TABLE " + allHeaders[0] + " ( " + headerOutput + " );")
    conn.commit()
cur.close()
conn.close()
