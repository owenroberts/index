class Geneword():
	''' functions for getting words and definitions '''

	def random_gallery_word(self):
		return self.random_noun(), self.random_prefix()

	def random_noun(self):
		from random import choice
		noun_file = open('input/37,199.txt')
		nouns = noun_file.read().splitlines()
		return choice(nouns).rstrip().lower()

	def get_nouns(self, file):
		noun_file = open('input/' + file + '.txt')
		return noun_file.read().splitlines()

	def random_prefix(self):
		from random import choice
		prefix_file = open('input/pref.txt')
		prefixes = prefix_file.read().splitlines()
		return choice(prefixes).rstrip()

	def get_prefix_def(self, prefix):
		import csv
		prefix_def = ''
		with open('input/prefix.csv', 'rt') as f:
			reader = csv.reader(f)
			for row in reader:
				if row[0] == prefix:
					prefix_def = row[1]
		return prefix_def

	def get_noun_defs(self, noun):
		from nltk.corpus import wordnet as wn
		sets = wn.synsets(noun, wn.NOUN)
		defs = []
		for s in sets:
			defs.append(s.definition())
		if len(sets) == 0:
			import csv
			with open('input/defs.csv', 'rt') as f:
				reader = csv.reader(f)
				for row in reader:
					if row[0] == noun:
						defs.append(row[1])
			if len(defs) == 0:
				defs.append("Not found.")
		return defs

	def get_prefixes(self):
		prefix_file = open("input/pref.txt")
		return prefix_file.read().splitlines() 

	def get_prefix_list(self, prefix):
		import csv
		prefix_list = []
		if '+' in prefix: # if more than one prefix
			prefixes = prefix.split('+')	
		else:
			prefixes = [prefix]
		for pref in prefixes:
				prefix_list.append({ "word": pref, "def":"" } )
		with open('input/prefix.csv', 'rt') as f:
			reader = csv.reader(f)
			for row in reader:
				for pref in prefix_list:
					if row[0] == pref["word"]:
						pref['def'] = row[1]

		# only for prefixes that are input by user
		if prefix_list[0]['def'] == "":
			from nltk.corpus import wordnet as wn
			def_sets = wn.synsets(prefix)
			if len(def_sets) > 0:
				prefix_list[0]['def'] = def_sets[0].definition()
			else:
				prefix_list[0]['def'] = "Not found."
		return prefix_list

if __name__ == '__main__':
	geneword = Geneword()