import os
import json
import sys
import copy	
import string
from string import punctuation
import re
from pprint import pprint

training_filename=sys.argv[1]

f=open(training_filename, "r").read().splitlines()

sentences=list()

classCountDict=dict()
classPriorProbDict=dict()
wordClassCountDict=dict()
wordClassProbDict=dict()
classDenDict=dict()
wordCountDict=dict()
modelDict=dict()

def removePunctuation(line):
	
	line_re = re.compile('[%s]' % re.escape(string.punctuation))
	line = line_re.sub(' ', line)
	return line
	

for line in f:
	line=copy.deepcopy(removePunctuation(line))
	sentences.append(line.split(' '))

sentenceCount=len(sentences)

def initializeClassDicts():
	classCountDict.update({'True':0})
	classCountDict.update({'Pos':0})
	classCountDict.update({'Fake':0})
	classCountDict.update({'Neg':0})
	classDenDict.update({'True':0})
	classDenDict.update({'Pos':0})
	classDenDict.update({'Fake':0})
	classDenDict.update({'Neg':0})




def initializeWordClassCount(word):
	wordClassCountDict[word]['True']=0
	wordClassCountDict[word]['Neg']=0
	wordClassCountDict[word]['Pos']=0
	wordClassCountDict[word]['Fake']=0

def processSentences():
	for sentence in sentences:
		classTag1=sentence[1]
		classTag2=sentence[2]
		sentence=sentence[3:]
		for word in sentence:
			word=word.lower()
			if word not in wordCountDict:
				wordCountDict[word]=1
			else:
				wordCountDict[word]+=1
			classDenDict[classTag1]+=1
			classDenDict[classTag2]+=1


			if word not in wordClassCountDict:
				wordClassCountDict[word]={}
				initializeWordClassCount(word)

			wordClassCountDict[word][classTag1]+=1
			wordClassCountDict[word][classTag2]+=1


		classCountDict[classTag1]+=1
		classCountDict[classTag2]+=1

def calculatePriorClassProb():
	classPriorProbDict['True']=classCountDict['True']/sentenceCount
	classPriorProbDict['Neg']=classCountDict['Neg']/sentenceCount
	classPriorProbDict['Pos']=classCountDict['Pos']/sentenceCount
	classPriorProbDict['Fake']=classCountDict['Fake']/sentenceCount


def calculateWordClassProb():
	
	numberOfWords=len(wordClassCountDict)
	for key in wordClassCountDict.keys():
		wordClassProbDict[key]={}
		for tag in wordClassCountDict[key].keys():
			prob=(wordClassCountDict[key][tag]+1)/(classDenDict[tag]+numberOfWords)
			wordClassProbDict[key].update({tag:prob})


def myPrint():
	print(sentences)
	pprint(classCountDict)
	pprint(classPriorProbDict)
	pprint(wordClassCountDict)
	pprint(wordClassProbDict)
	pprint(classDenDict)

def writeJSON():
	modelDict['Class Prob']=classPriorProbDict
	modelDict['Word Counts']=wordCountDict
	modelDict['Word Probabilites']=wordClassProbDict
	with open("nbmodel.txt", 'w', encoding="utf8") as f_out:
		json.dump(modelDict, f_out)

	f_out.close()


initializeClassDicts()
processSentences()
calculatePriorClassProb()
calculateWordClassProb()
#myPrint()
writeJSON()