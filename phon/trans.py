import epitran
import codecs

epi = epitran.Epitran('spa-Latn')

f = codecs.open('input/genesis.txt', encoding="utf-8")
# o = open('input/genesis_ipa.txt', 'w')

for line in f[:10]:
	print(line) 
	t = epi.transliterate(line)
	print(t)
	# o.write(t.encode('utf8'))

# o.close()