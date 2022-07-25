
from flask import Flask, url_for, request,render_template,jsonify, send_file
from flask_bootstrap import Bootstrap

import spacy
from spacy.lang.en.examples import sentences 
nlp = spacy.load("en_core_web_sm")
from textblob import TextBlob


# Initialize App
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze',methods = ['GET','POST'])
def analyze():
    if request.method == "POST":
        #ANALYSIS 
        rawtext = request.form['rawtext']

        docx = nlp(rawtext)
        #tokens
        custom_tokens = [token.text for token in docx]
        for token in docx:
            print(token.text)
        #wordinfo
        #pos
        #entities
        #sentiment
    return render_template('index.html', custom_tokens= custom_tokens)

@app.route("/basic_api")
def basic_api():
    return render_template('index.html')

@app.route("/imagescloud")
def imagescloud():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('index.html')


if __name__ =='__main__':
    app.run(debug=True)