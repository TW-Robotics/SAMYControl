import os
import glob
import pydot
import pickle
import numpy as np
import pprint

X_Train_FilesArray = glob.glob('./examples/*/.benchmark_suite/*/X_train.npy')
Y_Train_FilesArray = glob.glob('./examples/*/.benchmark_suite/*/Y_train.npy')
extra_data_FilesArray = glob.glob('./examples/*/.benchmark_suite/*/extra_data.pickle')

#print(X_Train_FilesArray)
#print(Y_Train_FilesArray)
#print(extra_data_FilesArray)

fileNameToCheck = 'cartpole'
trainFilesCounter= 0
for fileName in X_Train_FilesArray:
   if fileNameToCheck in fileName:
       break
   else:
       trainFilesCounter = trainFilesCounter + 1

extraFilesCounter = 0
for fileName in extra_data_FilesArray:
   if fileNameToCheck in fileName:
       break
   else:
       extraFilesCounter = extraFilesCounter + 1

infile = open(extra_data_FilesArray[trainFilesCounter],'rb')
dataset = pickle.load(infile)
infile.close()

dataX = np.load(X_Train_FilesArray[trainFilesCounter])
dataY = np.load(Y_Train_FilesArray[trainFilesCounter])

print('EXTRA DATA------------------------------------------')
pprint.pprint(dataset)
print('DATA X------------------------------------------')
pprint.pprint(dataX)
print('DATA Y------------------------------------------')
pprint.pprint(dataY)
