
from html.entities import entitydefs
import mimetypes
from os import sendfile
from xml.dom.minidom import Entity
from flask import Flask, url_for, request,render_template,jsonify, send_file
from flask_bootstrap import Bootstrap

import spacy
from spacy.lang.en.examples import sentences
import wordcloud 
nlp = spacy.load("en_core_web_sm")
from textblob import TextBlob

import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
from io import BytesIO
# Initialize App
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze',methods = ['GET','POST'])
def analyze():
    start = time.time()
    if request.method == "POST":
        #ANALYSIS 
        rawtext = request.form['rawtext']
        word_length = len(rawtext)

        docx = nlp(rawtext)
        #tokens
        custom_tokens = [token.text for token in docx]
        for token in docx:
            print(token.text)
        #wordinfo
        custom_wordinfo = [(token.text,token.lemma_,token.shape_,token.is_stop,token.is_alpha) for token in docx ]
        #pos
        custom_pos = [(word.text,word.tag_,word.pos_,word.dep_) for word in docx ]
        #entities
        custom_entities = [(entity.text, entity.label) for entity in docx.ents]
        #sentiment
        blob = TextBlob(rawtext)
        blob_sentiment = [(sentence.sentiment.polarity) for sentence in blob.sentences]
        blob_subjectivity = [(sentence.sentiment.polarity) for sentence in blob.sentences]
        result_json = json.dumps(custom_wordinfo,sort_keys=False,indent=3)
        end = time.time()
        final_time = end - start 
    return render_template('index.html',ctext= rawtext,final_time = final_time, custom_tokens= custom_tokens,custom_wordinfo=custom_wordinfo,
    result_json=result_json, custom_entities = custom_entities, blob_subjectivity=blob_subjectivity,blob_sentiment=blob_sentiment)

@app.route("/api")
def api():
    return render_template('restfulapidocs.html')

    #API TOKENS

@app.route('/api/tokens/<string:mytext>')
def api_tokens(mytext):
    docx = nlp(mytext)
    custom_tokens = [token.text for token in docx]
    return jsonify(custom_tokens)

    #API LEMMA

@app.route('/api/lemma/<string:mytext>')
def api_lemma(mytext):
    docx = nlp(mytext)
    custom_lemma = [(token.text,token.lemma_) for token in docx]
    return jsonify(custom_lemma)

    #API WORD INFO


@app.route('/api/wordinfo/<string:mytext>')
def api_wordinfo(mytext):
    docx = nlp(mytext)
    custom_wordinfo = ['token: {}, lemma:{}, shape:{}, is_stop: {}, is_alpha:{}'.format
    (token.text,token.lemma_,token.shape_,token.is_stop,token.is_alpha) for token in docx ]
    return jsonify(custom_wordinfo)

@app.route('/api/sentiment/<string:mytext>',methods=['GET'])
def api_sentiment(mytext):
	# Analysis
	blob = TextBlob(mytext)
	mysentiment = [ mytext,blob.words,blob.sentiment ]
	return jsonify(mysentiment)


@app.route("/images")
def imagescloud():
    return "<h2> Enter text into url eg. /fig/yourtext</h2>"

@app.route("/images/<mytext>")
def images(mytext):
    return render_template('images.html',title = mytext)

@app.route("/fig/<string:mytext>")
def fig(mytext):
    plt.figure(figsize=(20,10))
    wordcloud = WordCloud(background_color='white', mode ='RGB', width= 2000, height=1000).generate(mytext)
    plt.show()
    plt.axis('off')
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return sendfile(img, mimetypes='images/png')

@app.route("/about")
def about():
    return render_template('about.html')




if __name__ =='__main__':
    app.run(debug=True)