from nltk.corpus import wordnet as wn

nouns_file = open("../input/55,191.txt")
nouns = nouns_file.readlines()

f = open('non_proper_list_2.txt', 'w')

for noun in nouns:
	sets = wn.synsets(noun.strip(), wn.NOUN)
	use_word = False
	for set in sets:
		for lemma in set.lemma_names():
			if lemma[0].islower():
				use_word = True
	if use_word:
		f.write(noun)
f.close()