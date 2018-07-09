import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import os
#import shutil
import cython
from ripser import ripser, plot_dgms
#import wfdb
import multiprocessing as mp

NUM_WORKERS = 6





#Function to make the libary
#theDimension - what dimesnion should the perisistnce diagram go to
#numOfSec - the number of seconds should be used in the diagram
#ID - ID of the timeseries
#Path- the full path to the timeseries 

def setWindow(aStep,aListOfVals):
    theIndex = 0
    theLength = len(aListOfVals)
    theFinList = []
    if(theLength % aStep == 0):
        for i in range(0,theLength):
            if(theIndex <len(aListOfVals)):
                theFinList.append(aListOfVals[theIndex-1])
                theIndex += aStep
        
    return(theFinList)   

def makePersistDiagram(theDimension,numOfSec,ID,Path,Step):
    theX = []
    diagramss = ""
    #get the timeseries to the number of seconds
    theSamp = wfdb.rdsamp(Path  + ID)
    theData = theSamp[0]
    for i in range(0,len(theSamp[0])):
    #print(theSamp[0][i][0])
        theX.append(theSamp[0][i][0])
    theData = theX[0:numOfSec]
    print(theData)
    theData = setWindow(Step,theData)
    print(theData)
    theData = np.asarray(theData)
    #if even cuts 
    if(len(theData) % theDimension == 0):
        #setup set of vectors based off information given
        theFinData = theData.reshape(len(theData)//theDimension,theDimension)
        #print(theFinData)
        #use ripser and plot
        diagramsss = ripser(theFinData,theDimension)['dgms']
        plot_dgms(diagramss, show=True,save ="ID"+".jpg")

#rint(type(makePersistDiagram(50,3200,"A07872",'/home/dr-dunstan/Downloads/training2017/')))


#function to save from csv
def makeDiaFromCSV(dataType):
    #vairbles to deal with the csv and opening it 
    lineSkip = 0
    theCSV = open("200_set_of_Norm_AF_Rand.csv")
    
    #working the normal column of the csv
    if(dataType == "Normal"):
        #for each line in the csv
        for line in theCSV:
            #remove whitespace
            line = line.strip()
            #split up based off commas
            a,b,c,d = line.split(",")
            #if not at first line
            if(lineSkip != 0):
                #create plot diagram with ID at that line
                theSamp = wfdb.rdsamp("/home/dr-dunstan/Downloads/training2017/" + b)
                theData = len(theSamp[0])
                makePersistDiagram(2,theData,b,'/home/dr-dunstan/Downloads/training2017/')
            lineSkip += 1
#same with af & random
    elif(dataType == "AF"):
        for line in theCSV:
            line = line.strip()
            a,b,c,d = line.split(",")
            if(lineSkip != 0):
                theSamp = wfdb.rdsamp("/home/dr-dunstan/Downloads/training2017/" + c)
                theData = len(theSamp[0])
                theSamp2 = wfdb.rdsamp("/home/dr-dunstan/Downloads/training2017/" + b)
                theData2 = len(theSamp[0])
                theSamp3 = wfdb.rdsamp("/home/dr-dunstan/Downloads/training2017/" + d)
                theData3 = len(theSamp[0])
                makePersistDiagram(10,theData,c,'/home/dr-dunstan/Downloads/training2017/',5)
		makePersistDiagram(10,theData2,b,'/home/dr-dunstan/Downloads/training2017/',5)
		makePersistDiagram(10,theData3,d,'/home/dr-dunstan/Downloads/training2017/',5)
            lineSkip += 1
    elif(dataType == "Random"):
        for line in theCSV:
            line = line.strip()
            a,b,c,d = line.split(",")
            if(lineSkip != 0):
                theSamp = wfdb.rdsamp("/home/dr-dunstan/Downloads/training2017/"+ d)
                theData = len(theSamp[0])
                makePersistDiagram(2,theData,d,'/home/dr-dunstan/Downloads/training2017/')
            lineSkip += 1
    else:
        print("Datatype dosent exsit")


if __name__ == '__main__':
    jobs = []
    for i in range(10):
        p = mp.Process(target=makeDiaFromCSV, args=("AF"))
        jobs.append(p)
        p.start()


#makeDiaFromCSV("Normal")
