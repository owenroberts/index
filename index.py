from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/text')
def text():
	import text
	data = text.generateText( request.args['text'] )
	print(data['poem'])
	return render_template(
		"text.html", 
		newtext = data['lines'][:3],
		mark = data['poem']
	)

if __name__ == '__main__':
	#app.run(debug=True)
	app.run()