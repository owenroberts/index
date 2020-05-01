# coding: utf-8

from lib.mark_letter_switch import MarkovGenerator as LetterGen
from lib.mark_line import MarkovGenerator as WordGen
import codecs
import sys
import regex as re
import subprocess
# import string

colors = {
	'end': '\033[0m',
	0: '\033[95m',
	1: '\033[94m'
}

f1 = codecs.open('input/genesis_esp_ipa.txt', encoding="utf-8").readlines()
f2 = codecs.open('input/genesis_ipa.txt', encoding="utf-8").readlines()

files = [f1, f2]

# get the lower text line num
lineNum = min(len(f1), len(f2))

try:
	num = int(sys.argv[1])
except IndexError:
	num = 3
try:
	m = int(sys.argv[2])
except IndexError:
	m = 10

gen = LetterGen(n=num, max=m) # WordGen(n=num, max=m)

def byletter():
	for index, file in enumerate(files):
		for line in file[:lineNum]:
			line = line.strip()
			line = re.sub('[\p{P}\p{Sm}]+', '', line)
			# line.translate(dict.fromkeys(ord(c) for c in string.punctuation))
			words = line.split(" ")
			for word in words:
				gen.feed(word, index)

def byline():
	for file in files:
		for line in file:
			line = line.strip()
			gen.feed(line)


def text(n):
	for i in range(n):
		new = gen.generate()
		print new
		# outstring = ""
		# for n in new:
		# 	if type(n) is int:
		# 		outstring += colors[n]
		# 	else:
		# 		outstring += n
		# outstring += colors['end']
		# print outstring
		# subprocess.call(['flite -t', new])

byletter() # byline()
# gen.get_data()
text(10)

# for i in range(5):
# 	print gen.generate()

# print colors
# https://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

# strip punctuation
# https://stackoverflow.com/questions/33787354/strip-special-characters-and-punctuation-from-a-unicode-string

# tracking which text phonemes come from
	# randomly * trace the origin
	# email cmu guy
	# forcing back and forth


# lososospeneɾa
# los oso sos oso sos spe pen 

# syllable vs phoneme

# https://github.com/itinerarium/phoneme-synthesis
# http://tcts.fpms.ac.be/synthesis/mbrola.html
# http://www.tug.org/docs/liang/
# http://h6o6.com/2013/03/using-python-and-the-nltk-to-find-haikus-in-the-public-twitter-stream/
