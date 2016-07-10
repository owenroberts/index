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
	noun_file = open('input/somenouns.txt')
	nouns = noun_file.read().splitlines()
	noun = random.choice(nouns).rstrip().lower()
	return redirect( url_for('noun', origin = "random", noun = noun,  ) )

@app.route('/noun/<origin>/<noun>')
def noun(origin, noun):
	print origin, noun
	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.read().splitlines() 
	return render_template("noun.html", noun = noun, origin = origin, prefixes = prefixes )

@app.route('/newword/<noun>/<prefix>')
def newword(noun, prefix):
	prefixdef = ""
	import csv
	with open('input/prefix.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == prefix:
				prefixdef = row[1]
	return render_template("newword.html", prefix=prefix, noun=noun, prefixdef = prefixdef)

@app.route('/nouns/<num>')
def nouns(num):
	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.read().splitlines() 
	return render_template("nouns.html", num=num, prefixes=prefixes )

@app.route('/nouns/<num>/<prefix>')
def num_nouns(num, prefix):
	noun_file = open('input/'+num+'nouns.txt')
	nouns = noun_file.read().splitlines()
	return render_template("nouns-pref.html", num=num, nouns=nouns, prefix=prefix )


@app.route('/text')
def gen():
	print request
	if request.method == 'GET' and 'title' in request.args:
		return redirect( url_for('text', title = request.args['title'] ) )
	else:
		return render_template("gen.html")


@app.route('/text/<title>')
def text(title):
	import text
	data = text.generateText( title )
	print "me"
	print(data['poem'])
	return render_template(
		"text.html", 
		newtext = data['lines'][:8],
		mark = data['poem']
	)

if __name__ == '__main__':
	app.run(debug=True)
	#app.run()