#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import requests
import json

presence = False
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/surveillance')
def surveillance():
    return render_template('surveillance.html')

@app.route('/controle', methods=['GET', 'POST'])
def controle():
    return render_template('controle.html')

@app.route('/presence')
def get_presence():
    global presence
    presence = not presence
    return json.dumps(presence)

if __name__ == '__main__':
    app.run(debug=True)
