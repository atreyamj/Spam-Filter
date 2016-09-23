import os
import sys
import json
import math
jsonModel={}
spamDicts={}
hamDicts={}
spamProb=0.0
hamProb=0.0
##STASH
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
    spamWordCounts=[]
    spamCounts=[]
    spamProbab=[]
    for token in tokens:
        if token in spamDicts:
            spamWordCounts.append(spamDicts[token])
        else:
            if token in hamDicts:
                spamWordCounts.append(0)
            else:
                spamWordCounts.append(-1)
    for wordCounts in spamWordCounts:
        if wordCounts !=-1:
            spamCounts.append(wordCounts)
    for wordCounts in spamCounts:
        spamProbab.append(math.log((wordCounts + spamThreshold) / (jsonModel["spamWordTotal"] + jsonModel["uniqueWords"])))
    spamWordCounts = [spamDicts[token] if token in spamDicts else 0 if token in hamDicts else -1 for token in tokens]
    spamWordCounts = [wordCounts for wordCounts in spamWordCounts if wordCounts != -1]

    spamProbab = [math.log((wordCounts + spamThreshold)/ (jsonModel["spamWordTotal"] + jsonModel["uniqueWords"])) for wordCounts in spamWordCounts]
    totalSpamProbab = sum(spamProbab) + spamProbability
    return totalSpamProbab

def getHamProbability(hamProbability,fileContent):
    tokens = fileContent.split()
    hamWordCounts = []
    hamCounts = []
    hamProbab = []
    for token in tokens:
        if token in hamDicts:
            hamWordCounts.append(hamDicts[token])
        else:
            if token in spamDicts:
                hamWordCounts.append(0)
            else:
                hamWordCounts.append(-1)
    for wordCounts in hamWordCounts:
        if wordCounts != -1:
            hamCounts.append(wordCounts)
    for wordCounts in hamCounts:
        hamProbab.append(math.log((wordCounts + hamThreshold) / (jsonModel["hamWordTotal"] + jsonModel["uniqueWords"])))
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

def getPerformanceStatistics(outPutFileName):
    if not outPutFileName:
        return
    if len(outPutFileName) == 0:
        return
    results = []
    mappings = [[0, 0], [0, 0]]
    correctLabel=""
    predictLabel=""
    with open(outPutFileName) as outputModel:
        for inputLine in outputModel:
            index = inputLine.find(" ")
            if index <= len(inputLine):
                predictLabel = inputLine[0:index]
                pathOfFile = inputLine[index + 1:]
                nameOfFile = pathOfFile[pathOfFile.rfind("/") + 1:]
                if "ham" in nameOfFile:
                    correctLabel = "ham"
                else:
                    correctLabel = "spam"
                results = results + [(predictLabel, correctLabel)]

    for result in results:
        if (result[0] == result[1] and result[1] == "spam"):
            mappings[1][1] = mappings[1][1] + 1
        elif (result[0] == result[1] and result[1] == "ham"):
            mappings[0][0] = mappings[0][0] + 1
        elif (result[0] == "ham" and result[1] == "spam"):
            mappings[1][0] = mappings[1][0] + 1
        else:
            mappings[0][1] = mappings[0][1] + 1
    hamPrecision = mappings[0][0] / (mappings[0][0] + mappings[1][0])
    spamPrecision = mappings[1][1] / (mappings[1][1] + mappings[0][1])
    hamRecall = mappings[0][0] / (mappings[0][0] + mappings[0][1])
    spamRecall = mappings[1][1] / (mappings[1][1] + mappings[1][0])
    hamFscore = 2 * hamPrecision * hamRecall / (hamPrecision + hamRecall)
    spamFscore = 2 * spamPrecision * spamRecall / (spamPrecision + spamRecall)


if  len(sys.argv) != 2:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

if  not sys.argv[1]:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

buildModel("nbmodel.txt")
spamThreshold=jsonModel["spamMean"] / jsonModel["spamSD"]
hamThreshold=jsonModel["hamMean"] / jsonModel["hamSD"]
getClassification(sys.argv[1])
getPerformanceStatistics("nboutput.txt")
sys.exit(0)