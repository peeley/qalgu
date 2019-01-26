#!/usr/bin/python

import torch, pickle
from flask import Flask, render_template, request, jsonify
from src import evaluateSeq2Seq, langModel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/translate", methods = ['GET'])
def translate():
    inputString = request.args['q']
    translated = evaluateSeq2Seq.evaluate(inputString)
    translated = ' '.join(translated)
    translated = translated.replace('@', '').replace('/end/','')
    return jsonify(translated)

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.run()

