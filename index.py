from flask import Flask, request, render_template
import random
import nltk
nltk.download('punkt')
nltk.download('maxent_treebank_pos_tagger');
from nltk.tokenize import word_tokenize
from markov import MarkovGenerator

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/text')
def text():
	text = request.args['text']
	prefix_file = open("input/pref.txt")
	prefixes = prefix_file.readlines()
	file = open("input/"+text+".txt")
	lines = file.readlines()
	nountypes = ["NN", "NNP", "NNS", "NNPS"]
	punc = [".",",",";","?","-",]
	newlines = ""
	linelist = []
	for line in lines:
		tokens = nltk.word_tokenize(line)
		tagged = nltk.pos_tag(tokens)
		newline = line
		for idx, tag in enumerate(tagged):
			print(idx, tag)
			if any(tag[1] in n for n in nountypes):
				newword = random.choice(prefixes).rstrip().lower() + tag[0]
				newline = newline.replace(tag[0], newword)

		newlines += newline
		linelist.append( newline )
		#newlines += "\n"

	generator = MarkovGenerator(n=2, max=200)
	generator.feed(newlines)
	genpoem = generator.generate()
	genpoem = genpoem.split('\n')
	
	return render_template(
		"text.html", 
		newtext=linelist[:10],
		mark=genpoem
	)

if __name__ == '__main__':
	app.run(debug=True)