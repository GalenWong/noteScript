
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.tokenize import word_tokenize

salience = [{"black hole": 1}, {"black hole": 12, "dev":2}]


def mostImportantWord():
	#return "black holes"
	salienceDict = {}
	print(salience)
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

	print("biggest: ",  biggest)
	tokenizer = word_tokenize(biggest)
	
	lm = WordNetLemmatizer()

	result = ""
	for token in tokenizer:
		lemma = lm.lemmatize(token)
		result += lemma +" "

	result = result[:len(result)-1]

	return result


mostImportantWord()