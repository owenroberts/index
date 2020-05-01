import codecs
import sys
import regex as re

num = int(sys.argv[1])

f1 = codecs.open('input/genesis_ipa.txt', encoding="utf-8").readlines()
f2 = codecs.open('input/genesis_ipa.txt', encoding="utf-8").readlines()
files = [f1, f2]
lineNum = min(len(f1), len(f2))

ngrams = [list(), list()]

for index, file in enumerate(files):
	for line in file[:lineNum]:
		line = line.strip()
		line = re.sub('[\p{P}\p{Sm}]+', '', line)
		words = line.split(" ")
		for word in words:
			tokens = list(word)
			if len(tokens) > num:
				for i in range(len(tokens) - num):
					ngrams[index].append(tuple(tokens[i:i+num]))

count = 0

print len(ngrams[0])
print len(ngrams[1])

for n in ngrams[0]:
	if n in ngrams[1]:
		count += 1

print count