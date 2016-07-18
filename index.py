from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

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

@app.route('/noun')
def word_noun():
	return redirect( url_for('noun',  origin = request.args['origin'], noun = request.args['noun'] ) )

@app.route('/random')
def random():
	import random
	noun_file = open('input/1525.txt')
	nouns = noun_file.read().splitlines()
	noun = random.choice(nouns).rstrip().lower()
	return redirect( url_for('noun', origin = "random", noun = noun,  ) )

@app.route('/noun/<origin>/<noun>')
def noun(origin, noun):
	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.read().splitlines() 
	return render_template("noun.html", noun = noun, origin = origin, prefixes = prefixes )

@app.route('/new/<origin>/<noun>/<prefix>')
def newword(origin, noun, prefix):
	prefixdef = ""
	import csv
	with open('input/prefix.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == prefix:
				prefixdef = row[1]
	return render_template("newword.html", origin=origin, prefix=prefix, noun=noun, prefixdef = prefixdef)

@app.route('/new/<noun>/<prefix>')
def newword_orphan(noun, prefix):
	prefixdef = ""
	import csv
	with open('input/prefix.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == prefix:
				prefixdef = row[1]
	return render_template("newword.html", prefix=prefix, noun=noun, prefixdef = prefixdef)

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
	if (origin == "1525"):
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
def gen():
	if request.method == 'GET' and 'title' in request.args:
		return redirect( url_for('text', title = request.args['title'] ) )
	else:
		return render_template("gen.html")

@app.route('/text/<title>')
def text(title):
	import text
	data = text.generateText( title )
	return render_template(
		"text.html",
		title = title,
		newtext = data['lines'][:20],
		mark = data['poem']
	)

@app.route('/gallery/word')
def gallery_word():
	import random
	import csv
	noun_file = open('input/55,191.txt')
	nouns = noun_file.read().splitlines()
	noun = random.choice(nouns).rstrip().lower()
	
	prefix_file = open('input/pref.txt')
	prefixes = prefix_file.read().splitlines()
	prefix = random.choice(prefixes).rstrip().lower()

	prefixdef = ""
	with open('input/prefix.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == prefix:
				prefixdef = row[1]

	return render_template("gallery-word.html", prefix=prefix, prefixdef=prefixdef, noun=noun);


@app.route('/gallery/text')
def gallery_text():
	import text
	data = text.generateText( "genesis" )
	return render_template(
		"gallery-text.html",
		newtext = data['lines'][:8],
		mark = data['poem']
	)

if __name__ == '__main__':
	app.run(debug=True)
	#app.run()