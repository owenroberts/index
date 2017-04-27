import requests
from nltk.corpus import wordnet as wn
#noun_file = open('input/55,191.txt')
letter = 'b'
#noun_file = open('input/alpha/'+letter+'.txt')
noun_file = open('input/1525.txt')
nouns = noun_file.read().splitlines()
#nouns = ['test', 'butt', 'hello', 'world', 'tasdfaflc']
success = 0
fail = 0
alpha = "abcdefghijklmnopqrstuvwxyz"

# r = requests.get('https://en.wiktionary.org/w/api.php?action=query&prop=extracts&format=json&titles=test')
# if '-1' in r.json()['query']['pages']:
# 	print "in"
# else:
# 	print "out"

# generate alphabetical files
#d = {}
#alpha_count = 0
#noun_count = 0
#for noun in nouns:
#	if alpha_count < len( alpha ):
#		if noun_count == 0:
#			f = open( 'input/alpha/'+alpha[alpha_count]+'.txt', 'w+' )
#		if alpha[alpha_count] == noun[0]:
#			f.write( noun )
#			f.write('\n')
#			noun_count += 1
#		elif alpha[alpha_count] != noun[0]:
#			alpha_count += 1
#			noun_count = 0
#			f.close()


# f = open('input/wiki/'+letter+'.txt', 'w+')

for noun in nouns:
	#r = requests.get('https://api.pearson.com/v2/dictionaries/#entries?headword='+noun)
	#if r.json()['count'] == 0:
	s = False
	# for index in range(len(noun)+1):
	# 	n = noun[:index].upper() + noun[index:]
	# 	r = requests.get('https://en.wiktionary.org/w/api.php?action=query&prop=extracts&format=json&titles='+n)
	# 	if '-1' in r.json()['query']['pages']:
	# 		s = False
	# 	else:
	# 		s = True
	# 		break

	sets = wn.synsets(noun, wn.NOUN)
	if len(sets) > 0:
		success += 1
		#f.write( noun )
		#f.write( '\n' )
		#print noun, "success", success
	else:
		fail += 1
		print noun, "fail", fail
		print wn.synsets(noun)
print "success", success
# f.close()