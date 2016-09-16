import os
import sys

spamDicts={}
hamDicts={}
spamProb=0.0
hamProb=0.0

def buildModel(modelName):
    global spamProb,hamProb
    isSpam=0
    isHam=0
    with open(modelName, 'r', encoding="latin1") as modelFile:
        lineCount=1
        for line in modelFile:
            for word in line.split("="):
                word = word.rstrip('\n').rstrip('\r')
                if lineCount == 1:
                    spamProb=float(word)
                elif lineCount == 2:
                    hamProb=float(word)
                else:
                    if word=="SPAM":
                        isSpam=1
                        isHam=0
                    elif word=="HAM":
                        isSpam=0
                        isHam=1
                    else:
                        tokenIndex=0
                        tokens=line.split(" ")
                        if(len(line.split(" "))==1):
                            if isSpam==1: # Not Required
                                spamDicts[" "]=float(line.lstrip("=").rstrip("\r").rstrip("\n"))
                            elif isHam==1:
                                hamDicts[" "]=float(line.lstrip("=").rstrip("\r").rstrip("\n"))
                        elif(len(tokens)==2):
                            if isSpam==1:
                                spamDicts[str(tokens[tokenIndex])]=float(tokens[tokenIndex+1])
                            elif isHam==1:
                                hamDicts[str(tokens[tokenIndex])]=float(tokens[tokenIndex+1])
                lineCount+=1

def getSpamProbability(word):
    global spamDicts
    if word in spamDicts:
        return spamDicts[word]
    return 0

def getHamProbability(word):
    global hamDicts
    if word in hamDicts:
        return hamDicts[word]
    return 0

def doClassifyDocument(fileName):
    spamProbab=0
    hamProbab=0
    global spamProb,hamProb
    with open(fileName, 'r',encoding= "latin1") as f:
        for line in f:
            for word in line.split(" "):
                word=word.rstrip('\n').rstrip('\r')
                spamProbab+=getSpamProbability(word)
                hamProbab+=getHamProbability(word)
        spamProbab+=spamProb
        hamProbab+=hamProb
        if spamProbab > hamProbab:
            return 0
        elif spamProbab < hamProbab:
            return 1
        else:
            return 2

def getClassification(directoryPath):
    for root, dirs, files in os.walk(directoryPath):
        path = root.split('/')
        for file in files:
            if file.endswith(".txt"):
                classifcationValue=doClassifyDocument(os.path.join(root,file))
                if classifcationValue ==0:
                    print(file + " - SPAM")
                elif classifcationValue ==1:
                    print(file + " - HAM")
                else:
                    print(file + " - Can't Classify")

if  len(sys.argv) != 2:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

if  not sys.argv[1]:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

buildModel("nbmodel.txt")
getClassification(sys.argv[1])

sys.exit(0)