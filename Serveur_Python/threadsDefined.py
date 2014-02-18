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

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html', error=False)

"""@app.route('/login', methods=['POST'])
def process_login():
    email, password = request.form['email'].lower(), request.form['password']
    user = User.objects(email=email).first()
    if user is None or not user.valid_password(password):
        app.logger.warning("Couldn't login : {}".format(user))
        return render_template('login.html', error=True, email=email)
    else:
        session['logged_in'] = user.email
    return redirect('/')"""

@app.route('/presence')
def get_presence():
    global presence
    presence = not presence
    return json.dumps(presence)

if __name__ == '__main__':
    app.run(debug=True)





