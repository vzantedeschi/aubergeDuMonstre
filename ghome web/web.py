from flask import Flask, render_template, request
import requests
import json


app = Flask(__name__)

@app.route('/')
def hello():
    clients = [1, 2, 3]
    return render_template('index.html', clients=clients)

@app.route('/surveillance.html')
def surveillance():
	p = False
	return render_template('surveillance.html', presence = p)
	
if __name__ == '__main__' :
	app.run(threaded=True)
	print "ok"