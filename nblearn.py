import os
import sys
import math
import pickle
spamDicts={}
hamDicts={}
spamCount=0
hamCount=0
def readSpamFile(fileName):
    global spamDicts,spamCount
    with open(fileName, 'r',encoding= "latin1") as f:
        for line in f:
            for word in line.split(" "):
                word=word.rstrip('\n').rstrip('\r')
                if word in spamDicts:
                    spamDicts[word]=spamDicts[word]+1
                else:
                    spamDicts[word] = 1
    spamCount+=1

def readHamFile(fileName):
    global hamDicts,hamCount
    with open(fileName, 'r',encoding= "latin1") as f:
        for line in f:
            for word in line.split(" "):
                word=word.rstrip('\n').rstrip('\r')
                if word in hamDicts:
                    hamDicts[word]=hamDicts[word]+1
                else:
                    hamDicts[word] = 1
    hamCount+=1

def generateModel(modelFileName):
    global spamDicts,hamDicts,spamCount,hamCount
    spamWordsCount=0
    hamWordsCount=0
    for key, value in spamDicts.items():
        if len(key)!=0:
            spamWordsCount+=int(value)
    for key, value in hamDicts.items():
        if len(key)!=0:
            hamWordsCount+=int(value)
    with open(modelFileName, "w",encoding="latin1") as modelFile:
        if spamCount==0:
            modelFile.write("0.00\n")
        else:
            modelFile.write(str((spamCount / (spamCount + hamCount))) + "\n")
        if hamCount==0:
            modelFile.write("0.00\n")
        else:
            modelFile.write(str((hamCount / (spamCount + hamCount))) + "\n")
        modelFile.write(("SPAM")+"\n")
        for key, value in spamDicts.items():
            if len(key)!=0:
                modelFile.write(key + " " + str(math.log10((value/spamWordsCount)))+"\n")
        modelFile.write(("HAM")+"\n")
        for key, value in hamDicts.items():
            if len(key)!=0:
                modelFile.write(key+ " " +str(math.log10(((value / hamWordsCount))))+"\n")

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

