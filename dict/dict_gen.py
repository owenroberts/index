from nltk.corpus import wordnet as wn
import random
import regex as re

prefix_file = open("../input/pref.txt")
prefixes = prefix_file.readlines()

f = open('dictionary_full.txt', 'w')
s = open('dictionary_sample.txt', 'w')

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
defs = {}
all_the_words = []

def hyp_paths():
	for synset in list(wn.all_synsets('n')):
		paths = list(synset.hypernym_paths())
		if len(paths) > 0:
			path = paths[0]
			if len(path) > 2:
				hyps = list(paths[0][2].lemma_names())
				# print "2", paths[0][2]
			elif len(path) > 1:
				hyps = list(paths[0][1].lemma_names())
			elif len(path) == 1:
				hyps = list(paths[0][0].lemma_names())
				# print hyps
			hyp = hyps[0]
			defs[key] = hyp.definition() # add hyp def
			if hyp not in index:
				index[hyp] = []
			lemmas = synset.lemma_names()
			for word in lemmas:
				if re.match(r'^[a-z]+$', word):
					if word not in all_the_words:
						all_the_words.append(word)
						count += 1
						index[second_level_hypernym].append(word)

def hyp_paths_one():
	for synset in list(wn.all_synsets('n')):
		paths = list(synset.hypernym_paths())
		if len(paths) > 0:
			path = paths[0]
			if len(path) > 2:
				hyp = path[2]
			elif len(path) > 1:
				hyp = path[1]
			else:
				hyp = path[0]
			key = hyp.lemma_names()[0]
			defs[key] = hyp.definition() # add hyp def
			if key not in index:
				index[key] = []
			word = synset.lemma_names()[0]
			if re.match(r'^[a-z]+$', word):
				if word not in all_the_words:
					all_the_words.append(word)
					index[key].append(word)

hyp_paths_one()

def short_paths():
	for synset in list(wn.all_synsets('n')):
		paths = list(synset.hypernym_paths())
		path = min(paths, key=len)
		
		if len(path) > 2:
			hyp = path[2]
		elif len(path) > 1:
			hyp = path[1]
		else:
			hyp = path[0]

		key = hyp.lemma_names()[0]
		if key not in index:
			index[key] = []
		defs[key] = hyp.definition() # add hyp def
		lemmas = synset.lemma_names()
		for word in lemmas:
			if re.match(r'^[a-z]+$', word):
				if word not in all_the_words:
					all_the_words.append(word)
					index[key].append(word)

cats = ['entity', 'location', 'abstraction', 'group', 'possession', 'state', 'psychological feature', 'act', 'event', 'phenomenon']
cat_defs = {'entity':'something having concrete existence; living or nonliving', 'location':'a point or extent in space', 'abstraction':'a concept formed by extracting common features from examples', 'group':'any number of entities (members) considered as a unit', 'possession':'anything owned or possessed', 'state':'the way something is with respect to its main attributes', 'psychological feature':'a feature of the mental life of a living organism', 'act':'something that people do or cause to happen', 'event':'something that happens at a given place and time', 'phenomenon':'any state or process known through the senses rather than by intuition or reasoning'}

def cat_paths():
	for synset in list(wn.all_synsets('n')):
		paths = list(synset.hypernym_paths())
		path = min(paths, key=len)
		for syn in reversed(path):
			if syn.lemma_names()[0] in cats:
				key = syn.lemma_names()[0]
				break
		if key not in index:
			index[key] = []
		lemmas = synset.lemma_names()
		for word in lemmas:
			if re.match(r'^[a-z]+$', word):
				if word not in all_the_words:
					all_the_words.append(word)
					index[key].append(word)


def file_write(text):
	f.write(text)
	s.write(text)

def build_dict():
	for key in index.keys():
		print key, len(index[key])
		file_write(key)
		file_write('\n')
		file_write(defs[key])
		file_write('\n\n')
		count = 0
		for word in index[key]:
			f.write(word)
			f.write('\n')
			if count < 10:
				s.write(word)
				s.write('\n')
			count = count + 1

		file_write('\n\n')
		file_write('* * *')
		file_write('\n\n')

build_dict()
f.close()
s.close()