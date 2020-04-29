from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
import re

text = open("input/comm-beginning.txt").read()
lines = text.splitlines()
noun_types = ["NN", "NNS"]

sents = sent_tokenize(lines[0])
tokens = word_tokenize(sents[0])
tagged = pos_tag(tokens)
new_sent = sents[0]

for tag in tagged:
	if any (tag[1] in n for n in noun_types):
		new_word = 'fart' + tag[0]
		new_sent = re.sub(r'(?<![>/])\b'+tag[0], '<a class="new-word" href="/new/'+new_word+'">' + new_word + '</a>', new_sent)
print new_sent