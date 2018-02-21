from nltk.corpus import wordnet as wn

sample = [ "modernization", "childlessness", "lindheimera", "hiddenness", "sardine", "corchorus", "wynette", "theremin", "pigman", "auricula", "lepidoptery", "emasculation", "newspaper", "vintager", "petrel", "yenisei", "brigit", "mastdont", "saintliness", "great"]

#def get_next_hypernym(set):


for noun in sample:
	sets = wn.synsets(noun, wn.NOUN)

	# number of synsets
	# print len(sets)

	# total lemmas
	lemmas = 0
	for set in sets:
		lemmas += len(set.lemmas())
	#print lemmas

	# number of hyponyms
	hyponyms = 0
	for set in sets:
		#print set.hyponyms()
		hyponyms += len(set.hyponyms())
	#print hyponyms

	# level of hypernyms
	hypernyms = 0
	for set in sets:
		print set.max_depth()
		#print set.lemmas()
		#print set.hypernyms()