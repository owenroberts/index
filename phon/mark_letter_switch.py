class MarkovGenerator(object):

	def __init__(self, n, max):
		self.n = n # order (length) of ngrams
		self.max = max # maximum number of elements to generate
		self.ngrams = [
			dict(), # ngrams as keys; next elements as values
			dict()
		]
		self.beginnings = [
			list(), # beginning ngram of every line
			list()
		]

	def tokenize(self, text):
		return list(text)

	def feed(self, text, index):
		tokens = self.tokenize(text)

		# discard this line if it's too short
		if len(tokens) < self.n:
			return

		# store the first ngram of this line
		beginning = tuple(tokens[:self.n])
		self.beginnings[index].append(beginning)

		for i in range(len(tokens) - self.n):
			gram = tuple(tokens[i:i+self.n])
			next = tokens[i+self.n] # get the element after the gram

			# if we've already seen this ngram, append; otherwise, set the
			# value for this key as a new list
			if gram in self.ngrams:
				self.ngrams[index][gram].append(next)
			else:
				self.ngrams[index][gram] = [next]

	# called from generate() to join together generated elements
	def concatenate(self, source):
		return "".join(source)

	# generate a text from the information in self.ngrams
	def generate(self):
		from random import choice
		
		# get a random line beginning; convert to a list. 
		index = choice([0,1])
		alt = 0 if index is 1 else 1
		current = choice(self.beginnings[index])
		output = list(current)

		for i in range(self.max):
			if current in self.ngrams[alt]:
				possible_next = self.ngrams[alt][current]
				next = choice(possible_next)
				output.append(next)
				# get the last N entries of the output; we'll use this to look up
				# an ngram in the next iteration of the loop
				current = tuple(output[-self.n:])
				alt = 0 if alt is 1 else 1
			else:
				break

		output_str = self.concatenate(output)
		return output_str
	  

if __name__ == '__main__':

	import sys

	generator = MarkovGenerator(n=3, max=10)
	for line in sys.stdin:
		line = line.strip()
		words = line.split(" ")
		for word in words:
			generator.feed(word)

	for i in range(14):
		print generator.generate()

