from flask import Flask, render_template, request
import requests
import json


app = Flask(__name__)

@app.route('/')
def hello():
    clients = [1, 2, 3]
    return render_template('index.html', clients=clients)

@app.route('/surveillance.html')
def surveillance(p):
    return render_template('surveillance.html', presence=p)

app.run(debug=True)