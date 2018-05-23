import os
import json
import sys
from pprint import pprint

training_fileName=sys.argv[1]

f=open(training_fileName, "r", encoding="utf8", errors="ignore").read().splitlines()

sentences=list()

####stores totals for calculating probabilities
tagCountDict=dict() #total count of each tag - {tag:count}
transitionCountDict=dict() #total count of transitions from each tag - {from_tag:count}}

wordTagCount=dict() # count of each tag for each word - {word:{tag:count}}
tagTransitionCount=dict() # count of each transition - {from_tag:{to_tag:count}}

transitionProbDict=dict()
emissionProbDict=dict()
probDict=dict()

tagList=list() # only tags in every sentence

for line in f:
	sentences.append(line.split(' '))


def constructWordTagCount():
	for sentence in sentences:
		lineTags=list() #tags in each line - temporary
		for word in sentence:
			wordTag=word.rsplit('/',1)

			#if not ((wordTag[1]=='NNP') or (wordTag[1]=='NNPS')):
			#	wordTag[0]=wordTag[0].lower()

			lineTags.append(wordTag[1])

			if wordTag[1] not in tagCountDict:
				tagCountDict.update({wordTag[1]:1})
			else:
				tagCountDict[wordTag[1]]+=1

			
			if wordTag[0] in wordTagCount:
				if wordTag[1] in wordTagCount[wordTag[0]]:
					wordTagCount[wordTag[0]][wordTag[1]]+=1
				else:
					wordTagCount[wordTag[0]][wordTag[1]]=1

			else: 
				tempDict=dict()
				tempDict[wordTag[1]]=1
				wordTagCount.update({wordTag[0]:tempDict})

		tagList.append(lineTags)
	#print(tagList)

def constructTagTransitionCount():
	tagTransitionCount['Start']={}
	tagTransitionCount['Stop']={}

	for line in tagList:

		if line[0] not in tagTransitionCount['Start']: 
			tagTransitionCount['Start'][line[0]]=1		
		else:
			tagTransitionCount['Start'][line[0]]+=1

		if line[-1] not in tagTransitionCount['Stop']:
			tagTransitionCount['Stop'][line[-1]]=1
		else:
			tagTransitionCount['Stop'][line[-1]]+=1


		
		for i in range(0,len(line)):

			if line[i] not in transitionCountDict:                   #storing totals, for final probability calculation
				transitionCountDict.update({line[i]:1})
			else:
				transitionCountDict[line[i]]+=1

			if not i==len(line)-1:
																	 #storing transition counts
				if line[i] in tagTransitionCount:
					if line[i+1] in tagTransitionCount[line[i]]:
						tagTransitionCount[line[i]][line[i+1]]+=1
					else:
						tagTransitionCount[line[i]][line[i+1]]=1 				
				else:
					tempDict=dict()
					tempDict[line[i+1]]=1
					tagTransitionCount.update({line[i]:tempDict})
	transitionCountDict['Start']=len(tagList)
	transitionCountDict['Stop']=len(tagList)

	for f_tag in transitionCountDict.keys():
		if f_tag not in tagTransitionCount:
			tagTransitionCount[f_tag]={}
		for t_tag in transitionCountDict.keys():
			if t_tag not in tagTransitionCount[f_tag]:
				if t_tag=='Start':
					pass
				else:
					tagTransitionCount[f_tag][t_tag]=0

				

def findTransitionProb():
	domainLength=len(transitionCountDict.keys())-2
	#print('domain length', domainLength)
	k=6
	for key in tagTransitionCount.keys():
		transitionProbDict[key]={}
		if key=='Stop':
			for val in tagTransitionCount['Stop']:
				prob=(tagTransitionCount[key][val]+k)/(transitionCountDict[val]+(k*domainLength))
				transitionProbDict[key][val]=prob
			
		else:
			for to in tagTransitionCount[key]:
				prob=(tagTransitionCount[key][to]+k)/(transitionCountDict[key]+(k*domainLength))
				transitionProbDict[key][to]=prob


def findEmissionProb():
	for word in wordTagCount.keys():
		emissionProbDict[word]={}
		for tag in wordTagCount[word]:
			prob=wordTagCount[word][tag]/tagCountDict[tag]
			emissionProbDict[word][tag]=prob

def findProbabilities():

	findTransitionProb()
	findEmissionProb()
	probDict['Emission']=emissionProbDict
	probDict['Transition']=transitionProbDict
	probDict['Tag_Count']=tagCountDict
	probDict['Transition_Count']=transitionCountDict
	probDict['Word_Tag_Count']=wordTagCount
	probDict['Tag_Transition_Count']=tagTransitionCount
	'''
	tagCountDict=dict() #total count of each tag - {tag:count}
	transitionCountDict=dict() #total count of transitions from each tag - {from_tag:count}}

	wordTagCount=dict() # count of each tag for each word - {word:{tag:count}}
	tagTransitionCount=dict()
'''

def Print():

	#print(wordTagCount)
	#print("Count of tags\n", tagCountDict)
	#print("Emission Probabilities\n", emissionProbDict)


	#print("\n\ntagTransitionCount\n") 
	#pprint(tagTransitionCount)
	#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~transitionCountDict\n")
	#pprint(transitionCountDict)
	#print("Transition Probabilities\n", transitionProbDict)
	#print('\ntransitionProbDict')
	#pprint(transitionProbDict)
	#print('\n\n', probDict)
	pass

def findUniqueTran():
	count=0
	for key in tagTransitionCount:
		for to in tagTransitionCount[key]:
			count+=1

	print("Unique transitions: ", count)


def writeJSON():
	with open("hmmmodel.txt", 'w', encoding="utf8") as f_out:
		#json.dump(probDict, f_out, ensure_ascii=False)
		#print(probDict)
		json.dump(probDict, f_out)

constructWordTagCount()
constructTagTransitionCount()
findProbabilities()
#Print()
#findUniqueTran()
writeJSON()
#pprint(tagTransitionCount['Stop'])
#print('\n')
#pprint(transitionCountDict)

#pprint(transitionProbDict['Stop'])


#print('unique tags')
#print(transitionCountDict.keys())

#pprint(emissionProbDict)
