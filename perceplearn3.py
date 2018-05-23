import os
import json
import sys
import copy	
import string
from string import punctuation
import re
import random
from pprint import pprint


training_filename=sys.argv[1]
#training_filename="train-labeled.txt"
#training_filename="train_test.txt"

f=open(training_filename, "r").read().splitlines()

sentences=list()
counts=dict()

uniqueWords=list()
weightsDict1=dict()
weightsDict2=dict()

weightsDict3=dict()
weightsDict4=dict()
sumWeightsDict3=dict()
sumWeightsDict4=dict()

vanillaModelDict=dict()
averagedModelDict=dict()

for line in f:
	#print(line)
	#line=copy.deepcopy(removePunctuation(line))
	sentences.append(line.split(' '))


for sentence in sentences:
	sentence=sentence[3:]
	for word in sentence:
		word=word.lower()
		if word not in counts:
			counts[word]=1
		else:
			counts[word]+=1
		if word not in uniqueWords:
			uniqueWords.append(word)
			weightsDict1[word]=0
			weightsDict2[word]=0

b1=0
b2=0

for counter in range(0,15):
		for sentence in sentences:
			#print(len(sentence))
			a1=0
			a2=0
			wordCountDict=dict()
			classTag1=sentence[1]
			classTag2=sentence[2]
			sentence=sentence[3:]

			if classTag1=='True':
				y1=1
			else:
				y1=-1

			if classTag2=='Pos':
				y2=1
			else:
				y2=-1

			for word in sentence:

				
					word=word.lower()

					if word not in wordCountDict:
						wordCountDict[word]=1
					else:
						wordCountDict[word]+=1

			for word in wordCountDict.keys():
		
				a1=a1+wordCountDict[word]*weightsDict1[word]
				a2=a2+wordCountDict[word]*weightsDict2[word]
	

			a1=a1+b1
			a2=a2+b2

			if (a1*y1) <=0:
				for word in wordCountDict.keys():
					weightsDict1[word]=weightsDict1[word]+(wordCountDict[word]*y1)
				b1=b1+y1

			if (a2*y2) <=0:

				for word in wordCountDict.keys():
					weightsDict2[word]=weightsDict2[word]+(wordCountDict[word]*y2)
				b2=b2+y2


vanillaModelDict['class1']=weightsDict1
vanillaModelDict['class2']=weightsDict2
vanillaModelDict['BIAS1']=b1
vanillaModelDict['BIAS2']=b2
vanillaModelDict['Counts']=counts


b3=0
b4=0
sumb3=0
sumb4=0
c=-1

for word in uniqueWords:
		weightsDict3[word]=0
		weightsDict4[word]=0
		sumWeightsDict3[word]=0
		sumWeightsDict4[word]=0

for counter in range(0,30):
		c=c+1
		for sentence in sentences:
			a3=0
			a4=0
			wordCountDict=dict()
			classTag1=sentence[1]
			classTag2=sentence[2]
			sentence=sentence[3:]

			if classTag1=='True':
				y3=1
			else:
				y3=-1

			if classTag2=='Pos':
				y4=1
			else:
				y4=-1
			
			for word in sentence:
				word=word.lower()
				if word not in wordCountDict:
					wordCountDict[word]=1
				else:
					wordCountDict[word]+=1

			for word in wordCountDict.keys():
		
				a3=a3+wordCountDict[word]*weightsDict3[word]
				a4=a4+wordCountDict[word]*weightsDict4[word]

			a3=a3+b3
			a4=a4+b4

			if (a3*y3) <=0:
				for word in wordCountDict.keys():
					weightsDict3[word]=weightsDict3[word]+(wordCountDict[word]*y3)
				b3=b3+y3
				
				for word in wordCountDict.keys():
					sumWeightsDict3[word]=sumWeightsDict3[word]+(y3*c*wordCountDict[word])
				sumb3=sumb3+(y3*c)

			if (a4*y4) <=0:
				for word in wordCountDict.keys():
					weightsDict4[word]=weightsDict4[word]+(wordCountDict[word]*y4)
				b4=b4+y4

				for word in wordCountDict.keys():
					sumWeightsDict4[word]=sumWeightsDict4[word]+(y4*c*wordCountDict[word])
				sumb4=sumb4+(y4*c)
		

for word in weightsDict1.keys():
	weightsDict3[word]=weightsDict3[word]-((1/c)*sumWeightsDict3[word])
		
for word in weightsDict2.keys():	
	weightsDict4[word]=weightsDict4[word]-((1/c)*sumWeightsDict4[word])

b3=b3-((1/c)*sumb3)
b4=b4-((1/c)*sumb4)


averagedModelDict['class1']=weightsDict3
averagedModelDict['class2']=weightsDict4
averagedModelDict['BIAS1']=b3
averagedModelDict['BIAS2']=b4
averagedModelDict['Counts']=counts


with open("vanillamodel.txt", 'w', encoding="utf8") as f_out1:
	json.dump(vanillaModelDict, f_out1)

f_out1.close()

with open("averagedmodel.txt", 'w', encoding="utf8") as f_out2:
	json.dump(averagedModelDict, f_out2)

f_out2.close()