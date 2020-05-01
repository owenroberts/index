from nltk.corpus import cmudict

import sys

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

w = sys.argv[1]
genesis = open('../input/genesis.txt').readlines()

d = cmudict.dict()
def nsyl(word):
	return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]] 

print d[w.lower()]

# can't get syllables
# can swap phonemes, but then what...




#genesis = open('../input/genesis.txt').readlines()




# https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word
# https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word/4103234#4103234
# https://gist.github.com/bradmerlin/5693904


# import pyphen
# dic = pyphen.Pyphen(lang='en')
# #print dic.inserted(w)
# for line in genesis:
# 	for word in line.split(" "):
# 		if hasNumbers(word) == False:
# 			print dic.inserted(word) # this doesn't really do it, Joseph and died