from flask import Flask, redirect, url_for, request, render_template
from flask_sslify import SSLify
import os
import geneword

app = Flask(__name__)
gen = geneword.Geneword()

bug = True

if "DYNO" in os.environ:
	# Always use SSL if the app is running on Heroku (not locally)
    sslify = SSLify(app, subdomains=True)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/geneword-about')
def geneword_about():
	return render_template("geneword-about.html")

@app.route('/word')
def word():
	return render_template("word.html")

@app.route('/input')
def input():
	return render_template("input.html")

@app.route('/multi')
@app.route('/multi/<noun>')
def crazy(noun=None):
	from random import choice
	from random import randint
	
	if noun is None:
		noun, prefix = gen.random_gallery_word()
	else:
		prefix = gen.get_random_prefix()

	num_prefixes = randint(1, 4)
	prefix_list = []
	for i in range(0, num_prefixes):
		pref = gen.get_random_prefix()
		while pref in prefix_list:
			pref = choice(prefixes).rstrip() # no duplicate prefixes
		prefix_list.append( pref )

	url = '/new/multi/' + noun + '/'
	for p in prefix_list[:-1]:
		url += p
		url += '+'
	url += prefix_list[-1]
	return redirect( url )

@app.route('/noun')
@app.route('/noun/<origin>')
@app.route('/noun/<origin>/<noun>')
def noun(origin=None, noun=None):

	origin = origin if origin else request.args['origin']
	if origin == 'random':
		noun = gen.get_random_noun()
	noun = noun if noun else request.args['noun']

	return render_template("noun.html", 
		noun = noun, 
		origin = origin, 
		prefixes = gen.get_prefixes() 
	)

@app.route('/new/<origin>/<noun>/<prefix>')
def new_word(origin, noun, prefix):
	defs = gen.get_noun_defs(noun)
	prefix_list = gen.get_prefix_list(prefix)
	return render_template("new.html", origin=origin, noun=noun, defs=defs, prefix_list=prefix_list )

@app.route('/new/<noun>/<prefix>')
def new_word_orphan(noun, prefix):
	defs = gen.get_noun_defs(noun)
	prefix_list = gen.get_prefix_list(prefix)
	return render_template("new.html", noun=noun, defs=defs, prefix_list = prefix_list)


@app.route('/nouns/<origin>')
def nouns(origin):
	return render_template("nouns.html", origin=origin, prefixes=gen.get_prefixes() )

@app.route('/nouns/<origin>/<prefix>')
def num_nouns(origin, prefix):
	prefix = request.args['prefix'] if prefix == 'input' else prefix
	# prefix = prefix if prefix else request.args['prefix']
	nouns = gen.get_nouns(origin)
	
	if (origin == "1,514"):
		return render_template("nouns-pref.html", origin=origin, nouns=nouns, prefix=prefix )
	else:
		alpha = "abcdefghijklmnopqrstuvwxyz"
		d = {}
		for letter in alpha:
			d[letter] = []
			d[letter+"num"] = 0
		count = 0
		for noun in nouns:
			if count < len( alpha ):
				d[ alpha[count] + "num" ] += 1;
				if alpha[count] == noun[0] and len( d[alpha[count]] ) < 25:
					d[alpha[count]].append( noun )
				elif alpha[count] != noun[0]:
					count += 1
		return render_template("alphabetical.html", alpha=alpha, origin=origin, prefix=prefix, d=d)

@app.route('/nouns/<origin>/<prefix>/<letter>')
def nouns_alpha(origin, prefix, letter):
	letternouns = [noun for noun in gen.get_nouns(origin) if noun[0] is letter]
	return render_template(
		"nouns-pref.html", 
		origin=origin, 
		nouns=letternouns, 
		prefix=prefix, 
		letter=letter 
	)

@app.route('/random_gallery_word')
def random_gallery_word():
	from flask import jsonify
	return jsonify(gen.random_gallery_word())

@app.route('/gallery/word')
@app.route('/gallery/word/')
@app.route('/gallery/word/<noun>/<prefix>')
def gallery_word(noun=None, prefix=None):

	referer = request.headers.get('Referer')

	# don't start slide show if it comes from the noun create page
	print(referer)
	if referer is not None:
		start_slideshow = 'noun' not in referer and 'text' not in referer
	else:
		start_slideshow = True

	if noun == None:
		noun, prefix = gen.random_gallery_word()

	defs = gen.get_noun_defs(noun)
	prefix_def = gen.get_prefix_def(prefix)

	return render_template("gallery-word.html", 
		prefix = prefix, 
		prefix_def = prefix_def, 
		noun = noun, 
		defs = defs,
		start_slideshow = start_slideshow,
		referer = referer
	)

@app.route('/text')
def text():
	if request.method == 'GET' and 'title' in request.args:
		return redirect( url_for('text', title = request.args['title'] ) )
	else:
		return render_template("text-input.html")

@app.route('/url')
def from_url():
	import urllib
	import text
	from bs4 import BeautifulSoup

	f = urllib.urlopen( request.args['url'] ).read()

	try:
		soup = BeautifulSoup( f, 'html.parser')
		text_from_url = ""
		for p in soup.find_all('p'):
			text_from_url += p.get_text()
		# data = text.generate_text( text_from_url )
		new_text = text.generate_text( text_from_url )

		return render_template(
			"text.html",
			title = soup.title.string,
			new_text = new_text
			# mark = data['poem']
		)
	except:
		return render_template(
			"gen.html",
			error = "Sorry, that URL did not load correctly.  Try another URL."
		)

@app.route('/gallery/paste', methods=['GET', 'POST'])
def paste():
	try:
		title = "pasted"
		new_text = gen.generate_text( request.form['text'] )
		return render_template(
			"gallery-text.html", title = title, new_text = new_text, show_back_btn = True
		)
	except:
		return render_template(
			"text-input.html",
			error = "Sorry, we encountered an Error.  Try another text."
		)

@app.route('/gallery/text')
@app.route('/gallery/text/')
@app.route('/gallery/text/<title>')
def gallery_text(title=None):
	from random import choice

	show_back_btn = title is not None

	title = title if title else choice(['genesis', 'a-day', 'the-waves', 'a-tale-of-two-cities', 'moby-dick', 'the-red-wheelbarrow'])

	new_text = gen.generate_text( gen.load_text_from_file( title ) )

	return render_template("gallery-text.html", title = title, new_text = new_text, show_back_btn = show_back_btn)

@app.route('/phon/input')
def phone_input():
	return render_template(
		'phon_input.html'
	)

@app.route('/phon/string')
def phon_trans():
	string = request.args['string']
	language = request.args['language']
	
	import re
	import epitran
	epi = epitran.Epitran(language)

	trans = epi.transliterate(string)
	line = trans.strip()
	line = re.sub(r'[\\p{P}\\p{Sm}]+', '', line) # match punctuation or math symbol
	words = line.split(" ")
	sentence = []
	for word in words:
		sentence.append(word)

	return render_template(
		'phon_string.html',
		string = string,
		sentence = trans,
		words = words
	)

@app.route('/phon/test')
def phon_test():
	import codecs
	import re
	gen_heb = codecs.open('phon/input/genesis_heb.txt', encoding="utf-8").readlines()
	gen_eng = codecs.open('phon/input/genesis.txt', encoding="utf-8").readlines()
	gen_heb_ipa = codecs.open('phon/input/genesis_heb_ipa.txt', encoding="utf-8").readlines()
	gen_eng_ipa = codecs.open('phon/input/genesis_ipa.txt', encoding="utf-8").readlines()

	first_sents = []
	first_sents.append( gen_eng[0] )
	first_sents.append( gen_eng_ipa[0] )
	first_sents.append( gen_heb[0] )
	first_sents.append( gen_heb_ipa[0] )
	
	sentences = []

	for sent in first_sents:
		_sent = sent.strip()
		_sent = re.sub(r'[\\p{P}\\p{Sm}]+', '', sent)
		words = _sent.split(' ')
		sentences.append({
			"sentence": sent,
			"words": words
		})


	return render_template(
		'phon.html',
		sentences = sentences
	)

@app.route('/phon')
def phon():
	from phon.mark_letter_switch import MarkovGenerator as Mark
	import codecs
	import re
	f1 = codecs.open('phon/input/genesis_heb_ipa.txt', encoding="utf-8").readlines()
	f2 = codecs.open('phon/input/genesis_ipa.txt', encoding="utf-8").readlines()
	files = [f1, f2]
	lineNum = min(len(f1), len(f2)) # get the lower text line num
	gen = Mark(n=3, max=20)
	for index, file in enumerate(files):
		for line in file[:lineNum]:
			line = line.strip()
			line = re.sub(r'[\\p{P}\\p{Sm}]+', '', line) # match punctuation or math symbol
			words = line.split(" ")
			for word in words:
				gen.feed(word, index)
	sentences = []
	for i in range(5):
		words = []
		for j in range(10):
			new = gen.generate()
			words.append(new)
		# also include transliterated sentence ...
		sentences.append({
			"sentence": " ".join(words),
			"words": words
		})

	return render_template(
		'phon.html',
		sentences = sentences
	)

@app.route('/phon/choice')
def choice():
	import codecs
	f1 = codecs.open('phon/input/genesis_ipa.txt', encoding="utf-8").readlines()
	return render_template(
		'choice.html',
		text = f1[:10]
	)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def handle_500(e):
	print('500 error', e)
	return render_template("500.html", referrer = request.headers.get('Referer')), 500
	

if __name__ == '__main__':
	app.run(debug=bug)
