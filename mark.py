import sys
reload(sys)
sys.setdefaultencoding('utf8')
from markov import MarkovGenerator

file = open("input/"+sys.argv[1])
lines = file.readlines()

generator = MarkovGenerator(n=2, max=3000)
for line in lines:
	generator.feed(line)
text = generator.generate()
print text