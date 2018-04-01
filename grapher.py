from __future__ import print_function
import networkx as nx 
import matplotlib.pyplot as plt
import nlp
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.tokenize import word_tokenize


target = "A galaxy has black holes. The universe contains black holes. Black holes are regions and have strong gravity. Region is space and doesn't let light escape."
#target ="One of the consequences of Einstein’s general theory of relativity was a solution in which space-time curved so much that even a beam of light became trapped. These solutions became called black holes, and the study of them is one of the most intriguing fields of cosmology. Application of string theory to study black holes is one of the most significant pieces of evidence in favor of string theory."
#target ="One of the consequences of Einstein’s general theory of relativity was a solution in which space-time curved so much that even a beam of light became trapped."
sentences, salience = nlp.syntax_text(target.lower())

'''

sentence1 = {"galaxy": {"has":"black holes"}}
sentence2 = {"universe": {"contains":"black holes"}}
sentence3 = {"black holes":{"are":"region", "have":"strong gravity"}}
sentence4 = {"region":{"is":"space", "doesn't let": "light escape"}}
things = [sentence1,sentence2,sentence3,sentence4]
'''
def grapher(paragraphs, p_salience):

	nouns = []
	traversal_nouns = []
	para = paragraphs
	text = nx.DiGraph()
	salience = p_salience


	def addRemainingNodes():
		done = []
		for remaining in nouns:
			if remaining not in done:
				done.append(remaining)
				if not text.__contains__(remaining):
					text.add_node(remaining)
				remainingNodeHelper(remaining)

	def remainingNodeHelper(word):
		foundLink = False
		for sentence in para:
			if word in sentence:
				verbs = list(sentence[word].keys())
				for verb in verbs:
					obj = sentence[word][verb]
					if text.__contains__(obj):
						text.add_edge(obj, word, label = verb, weight = 1)
						uptrace(word)
						foundLink = True 
					else:
						text.add_edge(word, obj, label = verb, weight = 0)
						text.add_edge(obj, word, label = verb, weight = -1)
		return foundLink

	def uptrace(word):
		for node in text.neighbors(word):
			if text.edges[word, node]['weight'] == -1:
				text.remove_edge(parent, word)
				text.edges[word, node]['weight'] = 1
				uptrace(node)
	'''
	def main():
		findNouns()
		traversal_nouns = nouns
		makeGraph()
		addRemainingNodes()
		makeNotes(1, "black holes", False)
	'''
	def findNouns():
		for sentence in para:
			subject = list(sentence.keys())[0]
			nouns.append(subject)
			nouns.extend(sentence[subject].values())

	def makeGraph():
		topics = [mostImportantToken]
		insertNode(mostImportantToken)


	def insertNode (word):
		for sentence in para:
			if word in sentence:
				removeAll(word, nouns)
				verbs = list(sentence[word].keys())
				for verb in verbs:
					obj = sentence[word][verb]
					text.add_edge(word, obj, weight = 0, label = verb)
					if  obj != "":
						insertNode(obj)
					removeAll(obj, nouns)



	def removeAll (word, nouns):
		while nouns.count(word) != 0:
			nouns.remove(word)

	def mostImportantWord():
		#return "black holes"
		salienceDict = {}
		#print(salience)	
		for d in salience:
			for key in d:
				try:
					salienceDict[key] += d[key]
				except:
					salienceDict[key] = d[key]


		biggest = ""

		for k in salienceDict:
			if biggest == "":
				biggest = k

			elif salienceDict[k] > salienceDict[biggest]:
				biggest = k

		tokenizer = word_tokenize(biggest)
		
		lm = WordNetLemmatizer()

		result = ""
		for token in tokenizer:
			lemma = lm.lemmatize(token)
			result += lemma +" "

		result = result[:len(result)-1]
		print("biggest: ",  result)
		return result
		

	def makeNotes(tabCount, headNode, isParent):
		if not isParent:
			print (headNode)

		for child in text.neighbors(headNode):
			tabs = ""
			for x in range(0, tabCount):
				tabs += "\t"
			if  text.edges[headNode, child]['weight'] == 1:
				print (tabs + " - " + child + " " + text.edges[headNode, child]['label'] + " it/them")
				makeNotes(tabCount + 1, child, True)
			else:
				print (tabs + " - " + text.edges[headNode, child]['label'], end = ' ')
				makeNotes(tabCount + 1, child, False)
		
		

	mostImportantToken = mostImportantWord()
	findNouns()
	traversal_nouns = nouns
	makeGraph()
	addRemainingNodes()

	found = False
	for sentence in para:
		subjects = list(sentence.keys())
		for tokens in subjects:
			if mostImportantToken in tokens:
				mostImportantToken = tokens
				found = True
				break
		if found:
			break
	#nx.draw_networkx(text)
	#pos=nx.circular_layout(text)
	#nx.draw_networkx_nodes(text,pos,node_size=4500)
	#nx.draw_networkx_edges(text,pos,width=3.0)
	#nx.draw_networkx_labels(text,pos)
	#nx.draw_networkx_edge_labels(text,pos,edge_labels=nx.get_edge_attributes(text,'label'))
	#plt.title("Mind Map")
	#plt.axis('off')
	#plt.show()

	makeNotes(1, mostImportantToken, False)



grapher(sentences, salience)