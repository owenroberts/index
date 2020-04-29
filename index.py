from flask import Flask, redirect, url_for, request, render_template
from flask_sslify import SSLify
import os
import geneword

app = Flask(__name__)
gen = geneword.Geneword()

if "DYNO" in os.environ:
	# Always use SSL if the app is running on Heroku (not locally)
    sslify = SSLify(app, subdomains=True)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/word')
def word():
	return render_template("word.html")

@app.route('/input')
def input():
	print('input')
	return render_template("input.html")

@app.route('/noun')
def word_noun():
	return redirect( url_for('noun',  origin = request.args['origin'], noun = request.args['noun'] ) )

@app.route('/random')
def random():
	import random
	noun_file = open('input/37,199.txt')
	nouns = noun_file.read().splitlines()
	noun = random.choice(nouns).rstrip().lower()
	return redirect( url_for('noun', origin = "random", noun = noun ) )

@app.route('/multi')
def crazy():
	import random
	from random import randint
	import csv
	noun_file = open('input/37,199.txt')
	nouns = noun_file.read().splitlines()
	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.read().splitlines()
	num_prefixes = randint(2, 5)
	prefix_list = []
	for i in range(0, num_prefixes):
		# no duplicate prefixes
		pref = random.choice(prefixes).rstrip()
		while pref in prefix_list:
			pref = random.choice(prefixes).rstrip()
		prefix_list.append( pref )
	noun = random.choice(nouns).rstrip().lower()
	url = '/new/multi/' + noun + '/'
	for p in prefix_list[:-1]:
		url += p
		url += '+'
	url += prefix_list[-1]
	return redirect( url )

@app.route('/multi/<noun>')
def crazy_noun(noun):
	import random
	from random import randint
	import csv
	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.read().splitlines()
	num_prefixes = randint(2, 5)
	prefix_list = []
	for i in range(0, num_prefixes):
		# no duplicate prefixes
		pref = random.choice(prefixes).rstrip()
		while pref in prefix_list:
			pref = random.choice(prefixes).rstrip()
		prefix_list.append( pref )
	url = '/new/multi/' + noun + '/'
	for p in prefix_list[:-1]:
		url += p
		url += '+'
	url += prefix_list[-1]
	return redirect( url )

@app.route('/noun/<origin>/<noun>')
def noun(origin, noun):
	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.read().splitlines()
	print('orogin, noun', origin, noun)
	return render_template("noun.html", noun = noun, origin = origin, prefixes = prefixes )

@app.route('/new/<origin>/<noun>/<prefix>')
def new_word(origin, noun, prefix):
	defs = get_noun_defs(noun)
	prefix_list = get_prefix_list(prefix)
	return render_template("new.html", origin=origin, noun=noun, defs=defs, prefix_list=prefix_list )

@app.route('/new/<noun>/<prefix>')
def new_word_orphan(noun, prefix):
	defs = get_noun_defs(noun)
	prefix_list = get_prefix_list(prefix)
	return render_template("new.html", noun=noun, defs=defs, prefix_list = prefix_list)

def get_noun_defs(noun):
	from nltk.corpus import wordnet as wn
	sets = wn.synsets(noun, wn.NOUN)
	defs = []
	for s in sets:
		defs.append(s.definition())
	if len(sets) == 0:
		import csv
		with open('input/defs.csv', 'rt') as f:
			reader = csv.reader(f)
			for row in reader:
				if row[0] == noun:
					defs.append(row[1])
		if len(defs) == 0:
			defs.append("Not found.")
	return defs

def get_prefix_list(prefix):
	import csv
	prefix_list = []
	if '+' in prefix: # if more than one prefix
		prefixes = prefix.split('+')	
	else:
		prefixes = [prefix]
	for pref in prefixes:
			prefix_list.append({"word":pref, "def":""})
	with open('input/prefix.csv', 'rt') as f:
		reader = csv.reader(f)
		for row in reader:
			for pref in prefix_list:
				if row[0] == pref["word"]:
					pref['def'] = row[1]

	# only for prefixes that are input by user
	if prefix_list[0]['def'] == "":
		from nltk.corpus import wordnet as wn
		def_sets = wn.synsets(prefix)
		if len(def_sets) > 0:
			prefix_list[0]['def'] = def_sets[0].definition()
		else:
			prefix_list[0]['def'] = "Not found."
	return prefix_list

@app.route('/nouns/<origin>')
def nouns(origin):
	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.read().splitlines() 
	return render_template("nouns.html", origin=origin, prefixes=prefixes )

@app.route('/nouns/<origin>/<prefix>')
def num_nouns(origin, prefix):
	if prefix == "input":
		prefix = request.args['prefix']
	noun_file = open('input/'+origin+'.txt')
	nouns = noun_file.read().splitlines()
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
	noun_file = open('input/'+origin+'.txt')
	nouns = noun_file.read().splitlines()
	letternouns = []
	for noun in nouns:
		if letter == noun[0]:
			letternouns.append( noun )
	return render_template("nouns-pref.html", origin=origin, nouns=letternouns, prefix=prefix, letter=letter )


@app.route('/text')
@app.route('/text/<title>')
def text(title=None):
	import text

	if title == None:
		title = request.args['title']
	
	text_from_file = text.load_text_from_file(title)
	# data = text.generate_text( text_from_file )
	new_text = text.generate_text( text_from_file )


	return render_template(
		"text.html",
		title = title,
		new_text = new_text
	)
	

@app.route('/fromurl')
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

@app.route('/paste', methods=['GET', 'POST'])
def paste():
	import text
	try:
		new_text = text.generate_text( request.form['text'] )
		return render_template(
			"text.html",
			title = "text",
			new_text = new_text
		)
	except:
		return render_template(
			"gen.html",
			error = "Sorry, we encountered an Error.  Try another text."
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
	print(referer)

	#from_input = True # pause gallery if linked 
	# needs to look at referer
	start_slideshow = 'noun' not in referer
	# don't start slide show if it comes from the noun create page
	print('start_slideshow', start_slideshow)

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

@app.route('/gallery/text')
@app.route('/gallery/text/')
@app.route('/gallery/text/<title>')
def gallery_text(title=None):
	import text
	from random import choice

	title = title if title else choice(['genesis', 'a-day', 'the-waves', 'a-tale-of-two-cities', 'moby-dick', 'the-red-wheelbarrow'])

	text_from_file = text.load_text_from_file( title )

	new_text = text.generate_text( text_from_file )
	return render_template("gallery-text.html", new_text = new_text)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# @app.errorhandler(Exception)
# def handle_500(e):
# 	print(e)
# 	return render_template("500.html", referrer = request.headers.get('Referer')), 500
	

if __name__ == '__main__':
	app.run(debug=True)
	# app.run()
