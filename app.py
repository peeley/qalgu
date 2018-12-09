#!/usr/bin/python

import torch, pickle
from flask import Flask, render_template, request
from src import evaluateSeq2Seq, langModel

app = Flask(__name__)

print('Loading saved resources...')
savedEncoder = torch.load('src/encoder.pt')
savedDecoder = torch.load('src/decoder.pt')
with open('src/eng.p', 'rb') as testFile:
    testLang = pickle.load(testFile)
with open('src/ipq.p', 'rb') as targetFile:
    targetLang = pickle.load(targetFile)
print('Resources loaded.')

@app.route('/')
def index(result = 'Please enter phrase to be translated.'):
    return render_template('index.html', result = result)

@app.route("/translate", methods = ['GET','POST'])
def translate():
    if request.method == 'POST':
        inputString = [request.form['input']]
        translated = evaluateSeq2Seq.evaluate(savedEncoder, savedDecoder, inputString, testLang, targetLang)
        translated = ' '.join(translated)
        if translated:
            return index(translated)
        else:
            return index('ERROR: word not in vocabulary')
    else:
        return index()

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html')

@app.route('/warn')
def warn():
    return render_template('warn.html')

if __name__ == '__main__':
    app.run()
