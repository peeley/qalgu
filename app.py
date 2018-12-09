#!/usr/bin/python

import torch, pickle
from flask import Flask, render_template, request, jsonify
from src import evaluateSeq2Seq, langModel

app = Flask(__name__)

@app.route('/')
def index(result = ""):
    return render_template('index.html', result = result)

@app.route("/translate", methods = ['GET'])
def translate():
    string = request.args['q']
    inputString = [string]
    translated = evaluateSeq2Seq.evaluate(inputString)
    translated = ' '.join(translated)
    return jsonify(translated)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/warn')
def warn():
    return render_template('warn.html')

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.run()

# TODO: have html connect to translate API
