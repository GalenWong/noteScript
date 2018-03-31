import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "TryNLP-f5ba5437ac09.json"

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

client = language.LanguageServiceClient()

import json
import re
import six

def formPhrase(tokens, depend):
	dependIndex = -1
	left = []
	right = []
	for i in range(len(tokens)):
		if tokens[i].dependency_edge.head_token_index == depend:
			if i < depend:
				left = left + formPhrase(tokens, i)
			else:
				right=right + formPhrase(tokens, i)

	return left + [depend] + right


def breakToStruct(tokens, startI, endI):
	rootIndex = -1
	#subject = ""
	phrases = []

	for i in range(startI, endI):	# find the root
		#subject = subject + tokens[i].text.content + " "
		if str(tokens[i].dependency_edge.label) == '54':	# 54 IS ROOT
			rootIndex = i
			break
	
	for i in range(startI, endI):	# find the formPhrase from word that depend on rootIndex
		if i == rootIndex:
			continue
		if tokens[i].dependency_edge.head_token_index == rootIndex:
			phrases.append(formPhrase(tokens, i))


	result = {}

	'''
	result = {}
	result["subject"] = phrases[0]
	result["verb"] = []
	result["verb"].append(tokens[rootIndex].text.content)
	'''


def entities_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    print(entities)
    
    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))


def syntax_text(text):
	"""Detects syntax in the text."""
	client = language.LanguageServiceClient()

	if isinstance(text, six.binary_type):
		text = text.decode('utf-8')

	# Instantiates a plain text document.
	document = types.Document(
		content=text,
		type=enums.Document.Type.PLAIN_TEXT)

	# Detects syntax in the document. You can also analyze HTML with:
	#   document.type == enums.Document.Type.HTML
	result = client.analyze_syntax(document)
	tokens = result.tokens
	print(result)
	# part-of-speech tags from enums.PartOfSpeech.Tag
	pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

	for token in tokens:
		print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
                               token.text.content))

	start = 0
	R = []
	print("type of token:" + str(type(tokens)))
	for i in range(len(tokens)):
		if tokens[i].text.content == '.' or tokens[i].text.content == '?':
			R.append(breakToStruct(tokens, start, i+1))
			start = start + i + 1



	# result = []
	'''
	tokenDependReverse = list(range(len(tokens)))
	for i in range(len(tokens)):
		targetIndex = tokens[i].dependency_edge.head_token_index
		tokenDependReverse[targetIndex] = i


	print(tokenDependReverse)
	# get the last punc
	lastPunc = tokens[len(tokens)-1]

	firstDepend = lastPunc["dependency_edge"]["head_token_index"]

	endString = ""

	for i in range(firstDepend):
		endString+= token[i]["text"]["content"]
		endString+=" "

	endString += '\n\t'

	for i in range(firstDepend, len(tokens)):
	'''


str1 = "black hole is a region and has a gravitational field. Region is a space and blocks light."

syntax_text(str1)

'''

def isFreq(food):
	freqlist = ['BlueBerries', 'Lowfat Greek Yogurt','Mango','Pineapple']
	for i in freqlist:
		if i in food:
			return True
	return False


def getItemsByDiningHalls(name):
	jsonlist = os.listdir("ucla-dining-dataset/data/v2/")

	#removal = "Teriyaki Chicken|Spinach|Sesame|Miso Soup|Grilled Cheese|Chicken Breast|Cheese Pizza"

	menuItem = ""

	for i in jsonlist:
		data = json.load(open("ucla-dining-dataset/data/v2/" + i))
		for mealKey in data:
			for restaurant in data[mealKey]:
				if(restaurant["r"]==name):		#for specific restaurant			
					for kitchen in restaurant["rk"]:
						for items in kitchen["i"]:
							if(isFreq(items["e"])):
								continue
							menuItem+=items["e"]
							#addToDict(items["e"])

	return menuItem


def classify_text(text):
    """Classifies content categories of the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    categories = client.classify_text(document).categories

    for category in categories:
        print(u'=' * 20)
        print(u'{:<16}: {}'.format('name', category.name))
        print(u'{:<16}: {}'.format('confidence', category.confidence))

    print('\n\n')

    return categories


def pickInput():
	print("please input")
	print("B : Bruin Plate")
	print("C : Covel")
	print("D : De Neve")
	print("F : FEAST at Rieber")
	print("M : your own item")
	print("other key : quit")

	x = input()

	if x=='B':
		return getItemsByDiningHalls('Bruin Plate')[0:120000]
	elif x=='C':
		return getItemsByDiningHalls('Covel')[0:120000]
	elif x=='D':
		return getItemsByDiningHalls('De Neve')[0:120000]
	elif x=='F':
		return getItemsByDiningHalls('FEAST at Rieber')[0:120000]
	elif x=='M':
		print("your food: ")
		y = input()
		while len(y)<50000:
			y = 2 * y
		return y

	else:
		exit()



def loop(x):

	print('\n\n\n')


	result = classify_text(x)

	if not result:
		print('you typed nonsense...')
		return
	for i in result:

		name = i.name
		confidence = i.confidence
		print(name)
		print(confidence)
		if 'food' not in name.lower():
			print('This thing ain\'t even food you know')
			continue

		else:
			if confidence>0.8:
				print('literally best food ever')
			elif confidence>0.5:
				print('it is merely edible, okay')
			elif confidence>0.3:
				print('i am not sure whether you should eat that')
			else:
				print('imma say that ain\'t food')

		print('\n')

			
'''