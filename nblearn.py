import os
import sys
import json
import statistics
spamDicts={}
hamDicts={}

spamFileCount=0
hamFileCount=0
def readSpamFile(fileName):
    global spamDicts,spamFileCount
    with open(fileName, 'r',encoding= "latin1") as f:
        for line in f:
            for word in line.split():
                word=word.rstrip('\n').rstrip('\r')
                if (word in spamDicts):
                    spamDicts[word]=spamDicts[word]+1
                else:
                    spamDicts[word] = 1
    spamFileCount+=1

def readHamFile(fileName):
    global hamDicts,hamFileCount
    with open(fileName, 'r',encoding= "latin1") as f:
        for line in f:
            for word in line.split():
                word=word.rstrip('\n').rstrip('\r')
                if word in hamDicts:
                    hamDicts[word]=hamDicts[word]+1
                else:
                    hamDicts[word] = 1
    hamFileCount+=1

def generateModel(modelFileName):
    global spamDicts,hamDicts,spamFileCount,hamFileCount
    spamWordsCount=0
    hamWordsCount=0
    jsonData={}
    uniqueDict={}
    for key, value in spamDicts.items():
        if len(key)!=0:
            spamWordsCount+=int(value)
            uniqueDict[key]=0
    for key, value in hamDicts.items():
        if len(key)!=0:
            hamWordsCount+=int(value)
            uniqueDict[key] = 0
    if spamFileCount==0:
        jsonData["spamFileCount"]=0.00
    else:
        jsonData["spamFileCount"] = (spamFileCount)
    if hamFileCount==0:
        jsonData["hamFileCount"] = 0.00
    else:
        jsonData["hamFileCount"] = (hamFileCount)
    jsonData["SPAM"]= spamDicts
    jsonData["HAM"] = hamDicts
    jsonData["filesTotal"] = hamFileCount + spamFileCount
    jsonData["spamWordTotal"]=spamWordsCount
    jsonData["hamWordTotal"] = hamWordsCount
    jsonData["uniqueWords"] = len(uniqueDict)
    jsonData["spamMean"]=statistics.mean(spamDicts.values())
    jsonData["hamMean"] = statistics.mean(hamDicts.values())
    jsonData["spamSD"] = statistics.pstdev(spamDicts.values())
    jsonData["hamSD"] = statistics.pstdev(hamDicts.values())
    jsonString=json.dumps(jsonData,indent=4,sort_keys=True, ensure_ascii=False)
    with open(modelFileName, "w", encoding="latin1") as modelFile:
        modelFile.write(jsonString)


def listFiles(directoryPath):
    for root, dirs, files in os.walk(directoryPath):
        path = root.split('/')
        for file in files:
            if os.path.basename(root) == "spam":
                readSpamFile(os.path.join(root,file))
            if os.path.basename(root) == "ham":
             readHamFile(os.path.join(root,file))


if  len(sys.argv) != 2:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

if  not sys.argv[1]:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

listFiles(sys.argv[1])
generateModel("nbmodel.txt")
sys.exit(0);

