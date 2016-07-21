import random
import nltk
import re
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from markov import MarkovGenerator

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')


def generateText(text):
	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.readlines()
	file = open("input/"+text+".txt")
	lines = file.read().splitlines()
	nountypes = ["NN", "NNS"]
	punc = [".",",",";","?","-",]
	badwords = ['thee', 'hath']
	newtext = []
	for line in lines:
		#print "--", i
		sents = nltk.sent_tokenize( line )
		newgraf = ""
		for sent in sents:
			tokens = nltk.word_tokenize(sent)
			tagged = nltk.pos_tag(tokens)
			newsent = sent
			for idx, tag in enumerate(tagged):
				#print idx, tag
				if any(tag[1] in n for n in nountypes) and any(tag[0] not in b for b in badwords):
					pref = random.choice(prefixes).rstrip().lower()
					newword = pref + tag[0]
					newsent = re.sub(r'(?<![>/])\b'+tag[0], '<a href="/new/'+tag[0]+'/'+pref+'">' + newword + '</a>', newsent)
					#newsent = re.sub(r'(?<![>/])\b'+tag[0], newword, newsent, 1)
			newgraf += newsent + " "
		newtext.append( newgraf )
	
	generator = MarkovGenerator(n=2, max=2000)
	for lin in newtext:
		generator.feed( lin )
	genpoem = generator.generate()
	while len( genpoem ) < 100:
		genpoem = generator.generate()
	
	poemsents = nltk.sent_tokenize( genpoem )

	if len(poemsents) == 1:
		return { 'lines': newtext, 'poem': poemsents }
	if len(poemsents) > 0:
		return { 'lines': newtext, 'poem': poemsents[:-1] }
	else:
		return { 'lines': newtext, 'poem': genpoem }

if __name__ == '__main__':

	data = generateText(sys.argv[1])
	for line in data['lines'][:100]:
		print line

