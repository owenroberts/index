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
	return render_template("input.html")

@app.route('/multi')
@app.route('/multi/<noun>')
def crazy(noun=None):
	from random import choice
	from random import randint
	
	if noun is None:
		noun, prefix = gen.random_gallery_word()
	else:
		prefix = gen.random_prefix()

	num_prefixes = randint(1, 4)
	prefix_list = []
	for i in range(0, num_prefixes):
		pref = gen.random_prefix()
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
		noun = gen.random_noun()
	noun = noun if noun else request.args['noun']

	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.read().splitlines()

	return render_template("noun.html", 
		noun = noun, 
		origin = origin, 
		prefixes = prefixes 
	)

@app.route('/new/<origin>/<noun>/<prefix>')
def new_word(origin, noun, prefix):
	defs = gen.get_noun_defs(noun)
	prefix_list = get_prefix_list(prefix)
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

	prefix = prefix if prefix else request.args['prefix']
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

	# don't start slide show if it comes from the noun create page
	start_slideshow = 'noun' not in referer

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
