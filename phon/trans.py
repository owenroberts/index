import epitran
import codecs

epi = epitran.Epitran('spa-Latn')

f = codecs.open('input/genesis_esp.txt', encoding="utf-8")
o = open('input/genesis_esp_ipa.txt', 'w')

for line in f:
	#print line
	#print 
	t = epi.transliterate(line)
	o.write(t.encode('utf8'))

o.close()