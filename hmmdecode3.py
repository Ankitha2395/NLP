import os
import json
import copy
#import codecs
import sys
from math import log
from pprint import pprint

test_fileName=sys.argv[1]

probDict=json.load(open('hmmmodel.txt'))
emProb=copy.deepcopy(probDict['Emission'])
tranProb=copy.deepcopy(probDict['Transition'])
tagCountDict= copy.deepcopy(probDict['Tag_Count'])	#total count of each tag - {tag:count}
transitionCountDict=copy.deepcopy(probDict['Transition_Count'])	#total count of transitions from each tag - {from_tag:count}}
wordTagCount= copy.deepcopy(probDict['Word_Tag_Count'])	# count of each tag for each word - {word:{tag:count}}
tagTransitionCount=copy.deepcopy(probDict['Tag_Transition_Count'])	# count of each transition - {from_tag:{to_tag:count}}

f_input=open(test_fileName, "r", encoding="utf8", errors="ignore")
f_output=open("hmmoutput.txt","w", encoding="utf8")

f=f_input.read().splitlines()

sentences=list()
for line in f:
	sentences.append(line.split(' '))

finalTags=dict()
assignedTags=dict()

def findTags(word):
	if word in probDict['Emission']:
		tagList=list()
		for key in probDict['Emission'][word].keys():
			tagList.append(key)
		return tagList


def smoothWord(pos, word, sentence):
	#print('in Smooth word')
	#print('Word being smoothed...', word)
	emProb[word]={}
	if word.isdigit():
		emProb[word]['CD']=1.0
	elif len(word)==1 and word.isupper():
		emProb[word]['NN']=1.0
	elif word.endswith('.net') or word.endswith('.com'):
		emProb[word]['ADD']=1.0
	else:
		for tag in tagCountDict.keys():
			#print(tag)
			emProb[word][tag]={}
			emProb[word][tag]=1.0
	#pprint(emProb[word])



def calculateProb(prevWord, prevWord_tag, currWord, currWord_tag, index):

	### perform smoothing here ###

	#print('in calcProb')
	#print(prevWord, prevWord_tag, currWord, currWord_tag)

	#if currWord_tag not in tranProb[prevWord_tag]:
	#	transition_prob=0.0
		#smoothTransition()
	#else:
	

	if prevWord_tag=='Start':
		prevWord_tag_prob=1.0
	else:
		prevWord_tag_prob=finalTags[prevWord+'^'+str(index-1)][prevWord_tag][0]

	transition_prob=tranProb[prevWord_tag][currWord_tag]


	#if currWord not in emProb:
	#	currWord_emission_prob=0.0
	#else:
	#currWord=currWord.split('^')[0]
	currWord_emission_prob=emProb[currWord][currWord_tag]


	prob=(prevWord_tag_prob*transition_prob*currWord_emission_prob)

	return prob

def findMax(word, index):
	mp=0.0
	t=''
	for tags in finalTags[word+"^"+str(index)].keys():
		#print(tags)
		if finalTags[word+"^"+str(index)][tags][0]>mp:
			mp=finalTags[word+"^"+str(index)][tags][0]
			t=tags
	return t

def assignTags(sentence):
	#print('In assign tags...')
	#print('Taggging sentence...', sentence)
	prevTag=''
	string=""
	for i in range(len(sentence)-1, -1, -1):
		#print('Tagging word...', sentence[i])
		#print(sentence[i])

		if i==len(sentence)-1:
			prevTag=findMax(sentence[i], i)
			#print("prev tag", prevTag)
		
		#assignedTags[sentence[i]]=prevTag

		pair=sentence[i]+"/"+prevTag+" "
		string=pair+string
		#print('tag assigned', assignedTags[sentence[i]])
		#print('back pointer...', finalTags[sentence[i]+"^"+str(i)][prevTag][1])
		prevTag=finalTags[sentence[i]+"^"+str(i)][prevTag][1]

		#if prevTag not in finalTags[sentence[i]]:
		#	print('MY KEY ERROR')
		'''
			if len(finalTags[sentence[i]])==1:
				print('ONLY ONE VALUE AVAILABLE')
				for k in finalTags[sentence[i]]:
					print(k)
					prevTag=k
			else:
			
			m=0.0
			for k in finalTags[sentence[i]]:
				print('Possible tag',k)
				if finalTags[sentence[i]][k][0]>m:
					m=finalTags[sentence[i]][k][0]
					prevTag=k
					print('Assigning tag:', prevTag)
		'''

		#else:
		#prevTag=finalTags[sentence[i]][prevTag][1]
		#assignedTags[sentence[i]]=prevTag

	#pprint(assignedTags)
	#print(string)

	f_output.write(string+"\n")



def writeTags(sentence, last):
	
	string=""
	names=['Abbas','Nasser','Mahmoud','Buenos', 'Aires','san', 'francisco', 'california', 'mexico', 'Fiji', 'Miramar','Kerala', 'Jo', 'Deco', 'kerala', 'kollam', 'Varkala', 'Wellywood', 'auckland', 'iPhone', 'blackberry','Noida', 'afghanistan', 'Gretchen', 'Mustang', 'Pari', 'Chowk']
	names2=['Hannigan','Lucy','Elena','Klaus','Elijah','Katherine']
	#print('In write tags', sentence)
	for i in range(0,len(sentence)):
		#print(sentence[i])
		tag=assignedTags[sentence[i]]
		'''
		
		if 'www.' in sentence[i]:
			tag='ADD'
		if sentence[i] in names:
			tag='NNP'
		if sentence[i] in names2 or sentence[i].startswith('#'):
			tag='FW'
		if sentence[i].isdigit():
			tag='CD'
		'''
		'''
		if not sentence[i].isalpha():
			count=0
			dotCount=0
			for c in sentence[i]:
				if c.isdigit():
					count+=1
				if c=='.':
					dotCount+=1
			if dotCount==1:
				tag='CD'
			if count==len(sentence[i]):
				tag='CD'
		'''


		
		if not i==len(sentence)-1:
			string=string+sentence[i]+'/'+tag+" "

		else:
			if last:
				string=string+sentence[i]+'/'+tag
			else:
				string=string+sentence[i]+'/'+tag+'\n'
	#print(string)
	f_output.write(string)



def processSentence():
	for sentence in sentences:
		tagList=list()
		#tagDict=dict()
		for w in range(0, len(sentence)):
			tagList=findTags(sentence[w])
			incomingWord=sentence[w]+"^"+str(w)
			finalTags[incomingWord]={}

			if sentence[w] not in emProb:
				smoothWord(w, sentence[w], sentence)
			else:
				pass

			for currWord_tag in emProb[sentence[w]]:
				max_prob=0.0
				prev_tag=""
				if w==0:
					currWord_tag_prob=calculateProb(None, 'Start', sentence[w], currWord_tag,w)
					prev_tag='Start'
					'''
					if currWord_tag_prob>max_prob:
							max_prob=currWord_tag_prob
							prev_tag="Start"
					'''
					finalTags[incomingWord][currWord_tag]=(currWord_tag_prob,prev_tag)

				else:

					for prevWord_tag in finalTags[sentence[w-1]+"^"+str(w-1)].keys():

						currWord_tag_prob=calculateProb(sentence[w-1], prevWord_tag, sentence[w], currWord_tag,w)
						if currWord_tag_prob>max_prob:
							max_prob=currWord_tag_prob
							prev_tag=prevWord_tag
					finalTags[incomingWord][currWord_tag]=(max_prob,prev_tag)

		assignTags(sentence)
		'''
		if sentence==sentences[-1]:
			writeTags(sentence, 1)
		else:
			writeTags(sentence,0)
		'''



def Print():
	pprint(emProb)
	pprint(tranProb)
	#print(sentences)


	#pprint(finalTags)
	#pprint(assignedTags)

#Print()
processSentence()
#pprint(finalTags)




