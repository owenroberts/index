class MarkovGenerator(object):

	def __init__(self, n, max):
		self.n = n # order (length) of ngrams
		self.max = max # maximum number of elements to generate
		self.ngrams = dict() # ngrams as keys; next elements as values
		self.beginnings = list() # beginning ngram of every line

	def tokenize(self, text):
		return list(text)

	def feed(self, text, index):
		tokens = self.tokenize(text)

		# discard this line if it's too short
		if len(tokens) < self.n:
			return

		# store the first ngram of this line
		beginning = (index,) +  tuple(token for token in tokens[:self.n])
		self.beginnings.append(beginning)

		for i in range(len(tokens) - self.n):
			gram = (index,) +  tuple(token for token in tokens[:self.n])
			next = (index, tokens[i+self.n]) # get the element after the gram
			# if we've already seen this ngram, append; otherwise, set the
			# value for this key as a new list
			if gram in self.ngrams:
				self.ngrams[gram].append(next)
			else:
				self.ngrams[gram] = [next]

	# called from generate() to join together generated elements
	def concatenate(self, source):
		return source

	# generate a text from the information in self.ngrams
	def generate(self):
		from random import choice
		
		# get a random line beginning; convert to a list. 
		# just the letters
		start = choice(self.beginnings)
		current = start[1:]
		output = list(start)

		for i in range(self.max):
			# search both texts
			possible_next = []
			zero = (0,) + current
			one = (1,) + current
			if zero in self.ngrams:
				possible_next + self.ngrams[zero]
				# search other text for matches and add to possible
			if one in self.ngrams:
				possible_next += self.ngrams[one]
			if len(possible_next) > 0:
				next = choice(possible_next)
				
				# next search based on new tuple, use middle of current
				current = tuple(output[-self.n:-1])
				current += (next[1],)
				# plus next with text at end
				# this is the next ngram
				output += next

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

