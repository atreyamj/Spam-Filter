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
    spamProb= float(math.log10((jsonModel["spamFileCount"]/jsonModel["filesTotal"])))
    hamProb = float(math.log10((jsonModel["hamFileCount"] / jsonModel["filesTotal"])))

def getSpamProbability(word):
    global spamDicts,jsonModel
    if word in spamDicts:
        return float(math.log10(((spamDicts[word]+1))/(jsonModel["spamWordTotal"]+jsonModel["uniqueWords"])))
    return 0

def getHamProbability(word):
    global hamDicts
    if word in hamDicts:
        return float(math.log10(((hamDicts[word]+1)/(jsonModel["hamWordTotal"]+jsonModel["uniqueWords"]))))
    return 0

def doClassifyDocument(fileName):
    spamProbab=0
    hamProbab=0
    global spamProb,hamProb
    with open(fileName, 'r',encoding= "latin1") as f:
        for line in f:
            for word in line.split(" "):
                word=word.rstrip('\n').rstrip('\r')
                spamProbab=spamProbab+getSpamProbability(word)
                hamProbab=hamProbab+getHamProbability(word)
        spamProbab+=spamProb
        hamProbab+=hamProb
        if spamProbab > hamProbab:
            return 0
        elif spamProbab < hamProbab:
            return 1
        else:
            return 2

def getClassification(directoryPath):
    correctSpams=0
    correctHams=0
    classifiedSpams=0
    classifiedHams=0
    for root, dirs, files in os.walk(directoryPath):
        path = root.split('/')
        for file in files:
            if file.endswith(".txt"):
                classifcationValue=doClassifyDocument(os.path.join(root,file))
                if classifcationValue ==0:
                    if file.find("spam")!=-1:
                        correctSpams+=1
                    classifiedSpams+=1
                    print(file + " - SPAM")
                elif classifcationValue ==1:
                    if file.find("ham")!=-1:
                        correctHams+=1
                    classifiedHams+=1
                    print(file + " - HAM")
                else:
                    print(file + " - Can't Classify")
    #print("SPAM: "+str(correctSpams/classifiedSpams))
    #print("HAM: " + str(correctHams/ classifiedHams))
if  len(sys.argv) != 2:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

if  not sys.argv[1]:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

buildModel("nbmodel.txt")
getClassification(sys.argv[1])

sys.exit(0)