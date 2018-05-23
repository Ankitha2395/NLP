import os
import json
import sys
import copy	
import string
from string import punctuation
import re
from pprint import pprint
import operator
import random


#test_fileName="dev_test.txt"
#test_fileName="dev-text.txt"
#model_filename="vanillamodel.txt"
#model_filename="averagedmodel.txt"

model_filename=sys.argv[1]
test_fileName=sys.argv[2]


modelDict=json.load(open(model_filename))

weightsDict1=copy.deepcopy(modelDict['class1'])
weightsDict2=copy.deepcopy(modelDict['class2'])
b1=modelDict['BIAS1']
b2=modelDict['BIAS2']
counts=copy.deepcopy(modelDict['Counts'])


highFreq=dict()
highFreqWords=list()

stopWords=['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 
'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'dong', "don't", 'down', 'during', 
'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 
'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 
'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 
'same', "shan't", 'she', "she'd", "she'll", 's', "e's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 
'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 
'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', 
"who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']


f_input=open(test_fileName, "r", encoding="utf8", errors="ignore")

f_output=open("percepoutput.txt","w", encoding="utf8")

f=f_input.read().splitlines()
sentences=list()

def removePunctuation(line):
	'''
	line_re = re.compile('[%s]' % re.escape(string.punctuation))
	line = line_re.sub(' ', line)
	return line
	'''

	return ''.join(c for c in line if c not in punctuation)
'''
for line in f:
	line=copy.deepcopy(removePunctuation(line))
	line=copy.deepcopy(line.split())
	sentences.append(line)
'''
for line in f:
	#print(line)
	#line=copy.deepcopy(removePunctuation(line))
	sentences.append(line.split(' '))


def findHighFreqWords():
	highFreq = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)[:16]
	for pair in highFreq:
		highFreqWords.append(pair[0])

	#print(highFreqWords)



def findValues(wordCountDict):
	v1=0
	v2=0
	for word in wordCountDict.keys():

		if ((word not in weightsDict1)): #or (word in highFreqWords)): #or (word in stopWords)):
			#v1+=wordCountDict[word]
			v1+=0

		#if word in weightsDict1:
		else:
			v1+=wordCountDict[word]*weightsDict1[word]

		if ((word not in weightsDict2)): #or (word in highFreqWords)): #or (word in stopWords)):
			#v2+=wordCountDict[word]
			v2+=0

		else:
			v2+=wordCountDict[word]*weightsDict2[word]

	return v1,v2


def findClassTag(v1,v2):

		if v1<=0:
			classTag1='Fake'
		else:
			classTag1='True'

		if v2<=0:
			classTag2='Neg'
		else:
			classTag2='Pos'

		return classTag1, classTag2

def processSentence():
	#global b1
	#global b2
	for sentence in sentences:
		
		wordCountDict=dict()
		sentenceID=sentence[0]
		sentence=sentence[1:]

		for word in sentence:
			word=word.lower()
			if word=="":
				pass
			else:
				if word not in wordCountDict:
					wordCountDict[word]=1
				else:
					wordCountDict[word]+=1

		v1,v2=findValues(wordCountDict)
		v1=v1+b1
		v2=v2+b2

		classTag1, classTag2=copy.deepcopy(findClassTag(v1,v2))
		string=sentenceID+' '+classTag1+' '+classTag2+'\n'
		f_output.write(string)

findHighFreqWords()
processSentence()
