from nltk.corpus import wordnet as wn
import random

prefix_file = open("../input/pref.txt")
prefixes = prefix_file.readlines()
nouns_file = open("../input/55,191.txt")
nouns = nouns_file.readlines()

count = 0

for noun in nouns:
	p = random.choice(prefixes).strip()
	new_word = p + noun.strip()
	sets = wn.synsets(new_word, wn.NOUN)

	# this word is already a word (?)
	if len(sets) > 0:
		print ''
		#print new_word
		# for s in sets:
		#	print s.definition()

	else:
		if len(noun) > 15:
			count += 1
			print noun
			#print new_word


print count