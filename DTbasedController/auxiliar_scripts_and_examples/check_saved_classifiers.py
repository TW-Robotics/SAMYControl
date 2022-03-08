import os
import glob
import pydot
import pickle

dotFilesArray = glob.glob('./saved_classifiers/*/*/*.saved')

print(dotFilesArray)

fileNameToCheck = '/mc-aa/elevators'
fileCounter= 0
for fileName in dotFilesArray:
   if fileNameToCheck in fileName:
       break
   else:
       fileCounter = fileCounter + 1


print('\n--------------------------------------\n')
print(dotFilesArray[fileCounter])
print('\n--------------------------------------\n')

infile = open(dotFilesArray[fileCounter],'rb')
dt = pickle.load(infile)
infile.close()

print('\n--------------------------------------dt.__dict__\n')
print(dt.__dict__)
print('\n--------------------------------------dt.root.__dict__\n')
print(dt.root.children[0].__dict__)
print('\n--------------------------------------dt.root.splitting_strategies[0].__dict__\n')
print(dt.root.splitting_strategies[0].__dict__)
print('\n--------------------------------------dt.root.split\n')
print(dt.root.children[0].split)
print('\n--------------------------------------dt.root.split.__dict__\n')
print(dt.root.children[0].split.__dict__)

