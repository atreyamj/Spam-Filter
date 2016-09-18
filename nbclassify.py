import os
import sys
import json
import math
jsonModel={}
spamDicts={}
hamDicts={}
spamProb=0.0
hamProb=0.0

def buildModel(modelName):
    global spamProb,hamProb
    global spamDicts,hamDicts,jsonModel
    with open(modelName, 'r', encoding="latin1") as modelFile:
        jsonModel=json.load(modelFile)
    spamDicts= jsonModel["SPAM"]
    hamDicts = jsonModel["HAM"]
    spamProb= float(math.log((jsonModel["spamFileCount"]/jsonModel["filesTotal"])))
    hamProb = float(math.log((jsonModel["hamFileCount"] / jsonModel["filesTotal"])))


def getSpamProbability(spamProbability,fileContent):
    tokens = fileContent.split()
    spamWordCounts = [spamDicts[token] if token in spamDicts else 0 if token in hamDicts else -1 for token in tokens]
    spamWordCounts = [wordCounts for wordCounts in spamWordCounts if wordCounts != -1]

    spamProbab = [math.log((wordCounts + 1) / (jsonModel["spamWordTotal"] + jsonModel["uniqueWords"])) for wordCounts in spamWordCounts]
    totalSpamProbab = sum(spamProbab) + spamProbability
    return totalSpamProbab

def getHamProbability(hamProbability,fileContent):
    tokens = fileContent.split()
    hamWordCounts = [hamDicts[token] if token in hamDicts else 0 if token in spamDicts else -1 for token in tokens]
    hamWordCounts = [wordCounts for wordCounts in hamWordCounts if wordCounts != -1]

    hamProbab = [math.log((wordCounts + 1) / (jsonModel["hamWordTotal"] + jsonModel["uniqueWords"])) for wordCounts in hamWordCounts]
    totalHamProbab = sum(hamProbab) + hamProbability
    return totalHamProbab

def doClassifyDocument(fileName):
    global spamProb,hamProb
    filestream = open(fileName, "r", encoding="latin1")
    content = filestream.read()
    docSpamProb=getSpamProbability(spamProb, content)
    docHamProb = getHamProbability(hamProb, content)
    if docHamProb > docSpamProb:
        return 0
    elif docHamProb < docSpamProb:
        return 1

def getClassification(directoryPath):
    with open("nboutput.txt", "w", encoding="latin1") as nbout:
        for root, dirs, files in os.walk(directoryPath):
            path = root.split('/')
            for file in files:
                if file.endswith(".txt"):
                    classifcationValue=doClassifyDocument(os.path.join(root,file))
                    if classifcationValue ==0:
                        nbout.write("ham "+os.path.join(root,file)+"\n")
                    elif classifcationValue ==1:
                        nbout.write("spam "+os.path.join(root,file)+"\n")

if  len(sys.argv) != 2:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

if  not sys.argv[1]:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

buildModel("nbmodel.txt")
getClassification(sys.argv[1])

sys.exit(0)