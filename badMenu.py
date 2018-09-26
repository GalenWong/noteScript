import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "TryNLP-f5ba5437ac09.json"

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

client = language.LanguageServiceClient()

import json
import re
import six

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

			
