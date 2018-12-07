#!/usr/bin/python

import torch, pickle
from flask import Flask, render_template, request
from src import evaluateSeq2Seq
from src import langModel

app = Flask(__name__)

savedEncoder = torch.load('src/encoder.pt')
savedDecoder = torch.load('src/decoder.pt')
testLang = langModel.langModel('eng')
targetLang = langModel.langModel('ipq')
with open('src/eng.p', 'rb') as testFile:
    testLang = pickle.load(testFile)
with open('src/ipq.p', 'rb') as targetFile:
    targetLang = pickle.load(testFile)


@app.route('/')
def index(result = 'Please enter phrase to be translated.'):
    return render_template('index.html', result = result)

@app.route("/translate", methods = ['GET','POST'])
def translate():
    if request.method == 'POST':
        inputString = [request.form['input']]
        translated = evaluate(savedEncoder, savedDecoder, inputString, testLang, targetLang)
        if translated:
            return index(translated)
        else:
            return index('ERROR: word not in vocabulary')
    else:
        return index()

@app.errorhandler('404')
def pageNotFound():
    return render_template('404Error.html')

@app.route('/warn')
def warn():
    return render_template('warn.html')

if __name__ == '__main__':
    app.run()
