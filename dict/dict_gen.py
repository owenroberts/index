from nltk.corpus import wordnet as wn
import random
import regex as re

prefix_file = open("../input/pref.txt")
prefixes = prefix_file.readlines()

f = open('dictionary_full.txt', 'w')
# s = open('dictionary_sample.txt', 'w')

count = 0

# nouns_file = open("../input/55,191.txt")
# nouns = nouns_file.readlines()
# for noun in nouns:
# 	p = random.choice(prefixes).strip()
# 	new_word = p + noun.strip()
# 	sets = wn.synsets(new_word, wn.NOUN)
# 	if len(sets) > 0:
# 		count += 1
# 		print new_word
# 		for s in sets:
# 			print s.definition()

index = {}
all_the_words = []

for synset in list(wn.all_synsets('n')):

	paths = list(synset.hypernym_paths())
	
	if len(paths) > 0:
		if len(paths[0]) > 2:
			hyps = list(paths[0][2].lemma_names())
			# print "2", paths[0][2]
		elif len(paths[0]) > 1:
			hyps = list(paths[0][1].lemma_names())
		elif len(paths[0]) == 1:
			hyps = list(paths[0][0].lemma_names())
			# print hyps

		second_level_hypernym = hyps[0]
		if second_level_hypernym not in index:
			index[second_level_hypernym] = []

		lemmas = synset.lemma_names()
		for word in lemmas:
			if re.match(r'^[a-z]+$', word):
				if word in all_the_words:
					print "dup", word
				else: 
					all_the_words.append(word)
					count += 1
					index[second_level_hypernym].append(word)
			# else:
				# print word
		
	else:
		print "no paths", synset

	# print '--'
	# print count

for key in index.keys():
	print key, len(index[key])
	f.write(key)
	f.write('\n\n')
	for word in index[key]:
		f.write(word)
		f.write('\n')
	f.write('\n\n')
	f.write('* * *')
	f.write('\n\n')