class Geneword():
	''' functions for getting words and definitions '''

	def random_gallery_word(self):
		import random

		noun_file = open('input/37,199.txt')
		nouns = noun_file.read().splitlines()
		noun = random.choice(nouns).rstrip().lower()
		defs = self.get_noun_defs(noun)

		prefix_file = open('input/pref.txt')
		prefixes = prefix_file.read().splitlines()
		prefix = random.choice(prefixes).rstrip().lower()

		

		return noun, prefix

	def get_prefix_def(self, prefix):
		import csv
		with open('input/prefix.csv', 'rt') as f:
			reader = csv.reader(f)
			for row in reader:
				if row[0] == prefix:
					prefix_def = row[1]

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

if __name__ == '__main__':
	geneword = Geneword()