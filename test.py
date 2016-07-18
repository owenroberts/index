import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

text_file = open("zine/zine1.txt")
text = text_file.readlines()
nouns_file = open("input/allnouns.txt")
nouns = nouns_file.readlines()

for noun in nouns:
	for word in text:
		if (noun == word):
			print word

#f = open('zine/1525.txt', 'w')

print "done"