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
                        tokens=line.split("=")
                        if(len(line.split("="))==1):
                            if isSpam==1:
                                spamDicts[" "]=float(line.lstrip("=").rstrip("\r").rstrip("\n"))
                            elif isHam==1:
                                hamDicts[" "]=float(line.lstrip("=").rstrip("\r").rstrip("\n"))
                        elif(len(tokens)==2):
                            if isSpam==1:
                                spamDicts[str(tokens[tokenIndex])]=float(tokens[tokenIndex+1])
                            elif isHam==1:
                                hamDicts[str(tokens[tokenIndex])]=float(tokens[tokenIndex+1])
                lineCount+=1

buildModel("nbmodel.txt")
print(spamDicts["Subject:"])
sys.exit(0)