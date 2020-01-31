import random
prefix_file = open("../input/pref.txt")
prefixes = prefix_file.readlines()
nouns_file = open("../input/37,199.txt")
nouns = nouns_file.readlines()

url = "http://www.indexindexindex.com/new/" 

f = open('list.txt', 'w')

for noun in nouns:
	p = random.choice(prefixes).strip()
	href = url + noun.strip() + "/" + p
	line = p + noun.strip() + " " + href
	print line
	f.write(line)
	f.write('\n')
f.close()